import os
import json
import datetime
import pytz
from tqdm import tqdm
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import re
import time
import argparse
from tenacity import retry, stop_after_attempt, wait_exponential
import asyncio
from utils import (
    setup_logger, require_auth, is_original_repo,
    get_model_name, SUPPORTED_MODELS
)
from stats import analyze_papers
from tts import generate_daily_paper_audio
from newsletter import NewsletterGenerator

# 设置日志记录器
logger = setup_logger()

@require_auth
def init_api_client():
    """初始化并返回API客户端"""
    # 获取并验证 API Key
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        if is_original_repo():
            raise ValueError("原始仓库中未设置 DEEPSEEK_API_KEY 环境变量")
        else:
            raise ValueError("Fork仓库需要在 Settings -> Secrets -> Actions 中设置您自己的 DEEPSEEK_API_KEY")
    
    # 初始化客户端
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )

# 获取验证后的客户端
try:
    client = init_api_client()
except Exception as e:
    logger.error(f"API客户端初始化失败: {str(e)}")
    raise

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
@require_auth
def call_deepseek_api(prompt):
    """调用 DeepSeek API 的函数,包含重试机制"""
    try:
        # 获取配置的模型名称
        model_name = get_model_name()
        logger.info(f"使用模型: {SUPPORTED_MODELS.get(model_name, model_name)}")
        
        result = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的学术翻译助手。请保持翻译的准确性和专业性，使用恰当的学术术语。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=False
        )
        return result
    except Exception as e:
        if not is_original_repo():
            logger.error("如果您使用的是fork仓库，请确保已设置正确的DEEPSEEK_API_KEY")
        logger.error(f"API 调用出错: {str(e)}")
        raise

def create_poster(results, date_str, output_folder):
    # 创建海报
    width = 3200  # 增加宽度到最大
    min_height = 3200  # 相应增加最小高度
    background_color = (247, 247, 248)  # 浅灰背景
    primary_color = (255, 172, 51)  # HF 黄色
    secondary_color = (48, 76, 125)  # HF 蓝色
    text_color = (0, 0, 0)  # 黑色文字
    
    # 创建一个临时图像用于文本测量
    temp_image = Image.new('RGB', (width, 100), background_color)
    draw_test = ImageDraw.Draw(temp_image)
    
    # 加载字体
    try:
        if os.name == 'nt':  # Windows
            title_font = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 96)  # 增加字体大小
            content_font = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 56)  # 增加字体大小
        else:  # Linux/Mac
            # 尝试多个可能的字体路径
            font_paths = [
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/wqy-microhei/wqy-microhei.ttc",
                "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
            ]
            
            title_font = None
            content_font = None
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        title_font = ImageFont.truetype(font_path, 96)  # 增加字体大小
                        content_font = ImageFont.truetype(font_path, 56)  # 增加字体大小
                        print(f"成功加载字体：{font_path}")
                        break
                    except Exception as e:
                        print(f"尝试加载字体 {font_path} 失败：{e}")
            
            if title_font is None or content_font is None:
                raise Exception("未能找到可用的中文字体")
                
    except Exception as e:
        print(f"字体加载错误: {e}")
        print("使用默认字体")
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()

    # 计算所需的总高度
    y = 320  # 增加起始位置
    required_height = y  # 初始高度（包含顶部空间）
    
    # 预计算每篇论文所需的高度
    for result in results:
        # 提取中文标题和摘要
        translation = result.get("translation", "")
        
        # 使用更严格的正则表达式提取标题和摘要
        title_match = re.search(r"标题[:：]\s*([^\n]+)(?=\s*\n\s*摘要[:：]|\Z)", translation, re.DOTALL)
        summary_match = re.search(r"摘要[:：]\s*([^\n].+?)(?=\s*(?:\n\s*[^：\n]+[:：]|\Z))", translation, re.DOTALL)
        
        if not title_match:
            title_match = re.search(r"^([^\n]+)\n\s*摘要[:：]", translation, re.MULTILINE)
        
        title = (title_match.group(1) if title_match else "无标题").strip()
        summary = (summary_match.group(1) if summary_match else "").strip()
        
        if not summary and '摘要：' in translation:
            summary = translation.split('摘要：', 1)[1].strip()
        
        if not summary:
            summary = "无摘要"
            
        # 计算标题行数
        title_lines = []
        current_line = ""
        for word in title:
            test_line = current_line + word
            bbox = draw_test.textbbox((0, 0), test_line, font=content_font)
            if bbox[2] - bbox[0] <= width - 400:  # 增加标题宽度边距
                current_line = test_line
            else:
                if current_line:
                    title_lines.append(current_line)
                current_line = word
        if current_line:
            title_lines.append(current_line)
            
        # 计算摘要行数
        summary_lines = []
        current_line = ""
        for char in summary:
            current_line += char
            if len(current_line) >= 120:  # 增加每行字符数
                summary_lines.append(current_line)
                current_line = ""
        if current_line:
            summary_lines.append(current_line)
            
        # 计算这篇论文需要的高度
        paper_height = 120  # 增加基础高度（包含边距）
        paper_height += len(title_lines) * 60  # 增加标题行高
        paper_height += len(summary_lines) * 56  # 增加摘要行高
        paper_height += 80  # 增加额外边距
        
        required_height += paper_height
    
    # 添加底部边距和页脚空间
    required_height += 160
    
    # 确保最小高度
    height = max(min_height, required_height)
    
    # 释放临时资源
    del draw_test
    del temp_image
    
    # 创建适应内容的新图像
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    # 绘制顶部装饰条
    draw.rectangle([0, 0, width, 240], fill=primary_color)  # 增加顶部装饰条高度
    
    # 绘制标题
    title = f"Hugging Face {date_str} 论文日报"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    
    # 使用 HF logo
    try:
        logo_size = (96, 96)  # 增加 logo 大小
        logo_path = "hf_logo.png"
        logo = Image.open(logo_path).convert('RGBA')
        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)
        
        total_width = logo_size[0] + 20 + title_width  # 增加 logo 和标题间距
        start_x = (width - total_width) // 2
        
        image.paste(logo, (start_x, 72), logo)  # 调整 logo 位置
        draw.text((start_x + logo_size[0] + 20, 80), title, font=title_font, fill=(255, 255, 255))  # 调整标题位置
    except Exception as e:
        print(f"Logo加载错误: {e}")
        draw.text(((width - title_width) // 2, 80), title, font=title_font, fill=(255, 255, 255))
    
    # 绘制内容
    y = 320  # 增加内容起始位置
    for i, result in enumerate(results):
        # 提取中文标题和摘要
        translation = result.get("translation", "")
        
        title_match = re.search(r"标题[:：]\s*([^\n]+)(?=\s*\n\s*摘要[:：]|\Z)", translation, re.DOTALL)
        summary_match = re.search(r"摘要[:：]\s*([^\n].+?)(?=\s*(?:\n\s*[^：\n]+[:：]|\Z))", translation, re.DOTALL)
        
        if not title_match:
            title_match = re.search(r"^([^\n]+)\n\s*摘要[:：]", translation, re.MULTILINE)
        
        title = (title_match.group(1) if title_match else "无标题").strip()
        summary = (summary_match.group(1) if summary_match else "").strip()
        
        if not summary and '摘要：' in translation:
            summary = translation.split('摘要：', 1)[1].strip()
        
        if not summary:
            summary = "无摘要"
        
        # 创建论文卡片背景
        card_start_y = y
        
        # 计算卡片实际需要的高度
        title_lines = []
        current_line = ""
        for word in title:
            test_line = current_line + word
            bbox = draw.textbbox((0, 0), test_line, font=content_font)
            if bbox[2] - bbox[0] <= width - 400:  # 增加标题宽度边距
                current_line = test_line
            else:
                if current_line:
                    title_lines.append(current_line)
                current_line = word
        if current_line:
            title_lines.append(current_line)
        
        summary_lines = []
        current_line = ""
        for char in summary:
            current_line += char
            if len(current_line) >= 120:  # 增加每行字符数
                summary_lines.append(current_line)
                current_line = ""
        if current_line:
            summary_lines.append(current_line)
        
        # 计算这篇论文的实际高度
        card_height = 120  # 增加基础高度
        card_height += len(title_lines) * 60  # 增加标题行高
        card_height += len(summary_lines) * 56  # 增加摘要行高
        
        # 绘制卡片背景
        draw.rectangle([80, y, width-80, y+card_height], fill=(255, 255, 255))  # 调整卡片边距
        
        # 绘制序号
        circle_x = 160  # 调整序号位置
        circle_y = y + 60
        circle_radius = 40  # 增加序号圆圈大小
        draw.ellipse([circle_x-circle_radius, circle_y-circle_radius,
                     circle_x+circle_radius, circle_y+circle_radius],
                    fill=secondary_color)
        draw.text((circle_x, circle_y), str(i+1), font=content_font, fill=(255, 255, 255), anchor="mm")
        
        # 绘制标题
        title_x = 280  # 调整标题起始位置
        title_y = y + 40
        for i, line in enumerate(title_lines):
            draw.text((title_x, title_y + i*60), line, font=content_font, fill=text_color)
        
        # 绘制摘要
        summary_y = title_y + len(title_lines)*60 + 40
        for line in summary_lines:
            draw.text((160, summary_y), line, font=content_font, fill=text_color)  # 调整摘要起始位置
            summary_y += 56
        
        y += card_height + 30  # 更新下一个卡片的起始位置
    
    # 添加底部信息
    footer = "Generated by DeepSeek"
    footer_bbox = draw.textbbox((0, 0), footer, font=content_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) // 2, height - 80), footer, font=content_font, fill=text_color)
    
    # 保存图片
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{date_str}_poster.png")
    image.save(output_path)
    print(f"海报保存到：{output_path}")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def process_papers(date_str=None):
    """
    处理论文数据
    Args:
        date_str: 可选，指定要处理的日期，格式为YYYY-MM-DD。如果不指定，则使用当前日期。
    """
    try:
        # 如果没有指定日期，使用北京时间当前日期
        if date_str is None:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            current_time = datetime.datetime.now(beijing_tz)
            date_str = current_time.strftime('%Y-%m-%d')
        
        logger.info(f"正在处理 {date_str} 的论文数据")
        
        # 读取论文数据
        input_file = os.path.join('Paper_metadata_download', f"{date_str}.json")
        if not os.path.exists(input_file):
            logger.error(f"找不到 {date_str} 的论文数据文件")
            return False
            
        with open(input_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        if not papers:
            logger.warning(f"{date_str} 没有可用的论文数据")
            return False
            
        logger.info(f"读取到 {len(papers)} 篇论文数据")
        
        # 创建输出目录
        os.makedirs('HF-day-paper-deepseek', exist_ok=True)
        os.makedirs('posters', exist_ok=True)
        os.makedirs('newsletters', exist_ok=True)
        os.makedirs('audio', exist_ok=True)
        
        # 检查是否存在中间结果文件
        temp_file = os.path.join('HF-day-paper-deepseek', f"{date_str}_temp.json")
        if os.path.exists(temp_file):
            try:
                with open(temp_file, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                    processed_titles = {r['title'] for r in results}
                    logger.info(f"从中间文件恢复了 {len(results)} 篇已处理的论文")
            except Exception as e:
                logger.warning(f"读取中间文件失败: {str(e)}")
                results = []
                processed_titles = set()
        else:
            results = []
            processed_titles = set()
        
        success_count = len(results)
        error_count = 0
        
        # 处理每篇论文
        for index, paper in enumerate(papers, 1):
            try:
                # 获取论文信息
                paper_data = paper.get('paper', {})
                if not paper_data:
                    logger.warning(f"第 {index} 篇论文数据缺失")
                    error_count += 1
                    continue
                    
                title = paper_data.get('title', '')
                summary = paper_data.get('summary', '')
                paper_id = paper_data.get('id', '')
                url = f"https://huggingface.co/papers/{paper_id}"
                arxiv_url = f"https://arxiv.org/abs/{paper_id}" if paper_id else ""
                
                # 检查是否已处理过
                if title in processed_titles:
                    logger.info(f"第 {index} 篇论文已处理过，跳过")
                    continue
                
                if not title or not summary:
                    logger.warning(f"第 {index} 篇论文标题或摘要缺失")
                    error_count += 1
                    continue
                
                logger.info(f"正在处理第 {index}/{len(papers)} 篇论文")
                
                # 构建提示
                prompt = f"""请将以下论文标题和摘要翻译成中文，保持学术性和专业性：
                
                标题：{title}
                
                摘要：{summary}
                
                请按照以下格式返回：
                标题：[中文标题]
                摘要：[中文摘要]"""
                
                # 调用API进行翻译，带有重试机制
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        logger.info(f"正在翻译第 {index} 篇论文 (尝试 {retry_count + 1}/{max_retries})")
                        response = call_deepseek_api(prompt)
                        translation = response.choices[0].message.content
                        
                        # 验证翻译结果
                        if translation and '标题：' in translation and '摘要：' in translation:
                            break
                        else:
                            raise ValueError("翻译结果格式不正确")
                            
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            raise
                        logger.warning(f"第 {index} 篇论文翻译失败，将在 {2 ** retry_count} 秒后重试: {str(e)}")
                        time.sleep(2 ** retry_count)
                
                # 保存结果
                result = {
                    "title": title,
                    "summary": summary,
                    "translation": translation,
                    "url": url,
                    "arxiv_url": arxiv_url
                }
                results.append(result)
                processed_titles.add(title)
                success_count += 1
                
                # 保存中间结果
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                
                logger.info(f"第 {index} 篇论文处理成功")
                
                # 增加API调用间隔，避免限制
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"处理第 {index} 篇论文时发生错误: {str(e)}")
                error_count += 1
                continue
        
        logger.info(f"论文处理统计：总数 {len(papers)}，成功 {success_count}，失败 {error_count}")
        
        # 处理完成后，保存最终结果
        output_file = os.path.join('HF-day-paper-deepseek', f"{date_str}_HF_deepseek_clean.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 删除中间文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        # 如果成功处理了论文，继续生成其他内容
        if results:
            # 生成海报
            create_poster(results, date_str, 'posters')
            
            # 生成统计数据
            analyze_papers()
            
            # 生成通讯
            newsletter_gen = NewsletterGenerator()
            newsletter_gen.generate_newsletter(date_str)
            
            # 生成音频
            generate_daily_paper_audio(date_str)
            
            return True
        else:
            logger.error("没有成功处理任何论文")
            return False
            
    except Exception as e:
        logger.error(f"处理论文时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='处理HuggingFace每日论文数据')
    parser.add_argument('--date', type=str, help='指定要处理的日期 (YYYY-MM-DD格式)')
    args = parser.parse_args()

    # 使用指定的日期或默认使用当前日期
    success = process_papers(args.date)
    if not success:
        exit(1)
    exit(0) 
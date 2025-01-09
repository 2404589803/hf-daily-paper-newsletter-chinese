import os
import json
import datetime
import pytz
from tqdm import tqdm
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import re
import time
from tenacity import retry, stop_after_attempt, wait_exponential
import asyncio
from utils import setup_logger
from stats import analyze_papers
from tts import generate_daily_paper_audio
from newsletter import NewsletterGenerator

# 设置日志记录器
logger = setup_logger()

# 获取 DeepSeek API 密钥
api_key = os.getenv('DEEPSEEK_API_KEY')
if not api_key:
    raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_deepseek_api(prompt):
    """调用 DeepSeek API 的函数,包含重试机制"""
    try:
        result = client.chat.completions.create(
            model="deepseek-chat",
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
        print(f"API 调用出错: {str(e)}")
        raise

def create_poster(results, date_str, output_folder):
    # 创建海报
    width = 1200
    height = 1600
    background_color = (247, 247, 248)  # 浅灰背景
    primary_color = (255, 172, 51)  # HF 黄色
    secondary_color = (48, 76, 125)  # HF 蓝色
    text_color = (0, 0, 0)  # 黑色文字
    
    # 创建新图像
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    # 加载字体 - 支持多平台
    try:
        if os.name == 'nt':  # Windows
            title_font = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 48)
            content_font = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 28)
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
                        title_font = ImageFont.truetype(font_path, 48)
                        content_font = ImageFont.truetype(font_path, 28)
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
    
    # 绘制顶部装饰条
    draw.rectangle([0, 0, width, 120], fill=primary_color)
    
    # 绘制标题
    title = f"Hugging Face {date_str} 论文日报"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    
    # 使用 HF logo 替代表情符号
    try:
        # 加载并调整 HF logo 大小
        logo_size = (48, 48)  # 设置合适的logo大小
        logo_path = "hf_logo.png"  # 确保此文件存在
        logo = Image.open(logo_path).convert('RGBA')
        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)
        
        # 计算整体宽度和起始位置
        total_width = logo_size[0] + 10 + title_width  # 10是logo和文字之间的间距
        start_x = (width - total_width) // 2
        
        # 粘贴 logo
        image.paste(logo, (start_x, 36), logo)  # 36是为了垂直对齐
        # 绘制标题文字
        draw.text((start_x + logo_size[0] + 10, 40), title, font=title_font, fill=(255, 255, 255))
    except Exception as e:
        print(f"Logo加载错误: {e}")
        # 如果logo加载失败，回退到居中显示标题
        draw.text(((width - title_width) // 2, 40), title, font=title_font, fill=(255, 255, 255))
    
    # 绘制内容
    y = 160
    max_papers = 5  # 限制显示的论文数量
    
    for i, result in enumerate(results[:max_papers]):
        # 提取中文标题和摘要
        translation = result.get("translation", "")
        
        # 使用更严格的正则表达式提取标题和摘要
        title_match = re.search(r"标题[:：]\s*([^\n]+)(?=\s*\n\s*摘要[:：]|\Z)", translation, re.DOTALL)
        summary_match = re.search(r"摘要[:：]\s*([^\n].+?)(?=\s*(?:\n\s*[^：\n]+[:：]|\Z))", translation, re.DOTALL)
        
        # 如果匹配失败，尝试使用备用模式
        if not title_match:
            title_match = re.search(r"^([^\n]+)\n\s*摘要[:：]", translation, re.MULTILINE)
        
        title = (title_match.group(1) if title_match else "无标题").strip()
        summary = (summary_match.group(1) if summary_match else "").strip()
        
        # 如果摘要为空，尝试获取剩余的所有文本作为摘要
        if not summary and '摘要：' in translation:
            summary = translation.split('摘要：', 1)[1].strip()
        
        if not summary:
            summary = "无摘要"
        
        # 创建论文卡片背景
        card_height = 280  # 增加卡片高度
        draw.rectangle([30, y, width-30, y+card_height], fill=(255, 255, 255))
        
        # 绘制序号
        number_circle_radius = 20
        circle_x = 60
        circle_y = y + 30
        draw.ellipse([circle_x-number_circle_radius, circle_y-number_circle_radius,
                     circle_x+number_circle_radius, circle_y+number_circle_radius],
                    fill=secondary_color)
        draw.text((circle_x, circle_y), str(i+1), font=content_font, fill=(255, 255, 255), anchor="mm")
        
        # 绘制论文标题（支持多行）
        title_x = 120
        title_y = y + 20
        title_max_width = width - 150
        title_lines = []
        current_line = ""
        
        for word in title:
            test_line = current_line + word
            bbox = draw.textbbox((0, 0), test_line, font=content_font)
            if bbox[2] - bbox[0] <= title_max_width:
                current_line = test_line
            else:
                if current_line:
                    title_lines.append(current_line)
                current_line = word
        if current_line:
            title_lines.append(current_line)
        
        # 绘制标题（最多2行）
        for i, line in enumerate(title_lines[:2]):
            draw.text((title_x, title_y + i*30), line, font=content_font, fill=text_color)
        
        # 调整摘要起始位置
        summary_y = title_y + len(title_lines[:2])*30 + 20
        
        # 处理摘要文本换行
        max_chars_per_line = 42  # 增加每行字符数
        summary_lines = []
        current_line = ""
        
        for char in summary:
            current_line += char
            if len(current_line) >= max_chars_per_line:
                summary_lines.append(current_line)
                current_line = ""
        if current_line:
            summary_lines.append(current_line)
        
        # 绘制摘要（最多8行）
        max_summary_lines = 8  # 增加最大行数
        for line_idx, line in enumerate(summary_lines[:max_summary_lines]):
            draw.text((60, summary_y), line, font=content_font, fill=text_color)
            summary_y += 28  # 稍微减小行间距
            
            # 如果是最后一行且还有更多内容，添加省略号
            if line_idx == max_summary_lines - 1 and len(summary_lines) > max_summary_lines:
                draw.text((60, summary_y - 28), line[:-3] + "...", font=content_font, fill=text_color)
        
        y += card_height + 15  # 稍微减少卡片间距
    
    # 添加底部信息
    footer = "Generated by DeepSeek"
    footer_bbox = draw.textbbox((0, 0), footer, font=content_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) // 2, height - 40), footer, font=content_font, fill=text_color)
    
    # 保存图片
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{date_str}_poster.png")
    image.save(output_path)
    print(f"海报保存到：{output_path}")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def process_papers():
    """处理论文的主函数，包含重试机制"""
    try:
        # 获取昨天的日期
        beijing_tz = pytz.timezone('Asia/Shanghai')
        today = datetime.datetime.now(beijing_tz)
        yesterday = today - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        
        logger.info(f"开始处理 {yesterday_str} 的论文数据")
        
        # 读取元数据文件
        metadata_file = os.path.join('Paper_metadata_download', f"{yesterday_str}.json")
        if not os.path.exists(metadata_file):
            logger.error(f"未找到元数据文件：{metadata_file}")
            return
            
        with open(metadata_file, 'r', encoding='utf-8') as f:
            papers_data = json.load(f)
                
        results = []
        # 使用tqdm显示进度条
        for paper_str in tqdm(papers_data, desc="处理论文"):
            try:
                # 解析paper字符串为字典
                paper_data = eval(paper_str)
                paper_info = paper_data.get("paper", {})
                
                if not paper_info:
                    continue
                    
                title = paper_info.get("title", "")
                summary = paper_info.get("summary", "")
                
                # 调用DeepSeek API进行翻译
                prompt = f"""请将以下论文标题和摘要翻译成中文，保持学术性和专业性：

标题：{title}

摘要：{summary}

请按以下格式输出：
标题：[中文标题]
摘要：[中文摘要]"""
                
                result = call_deepseek_api(prompt)
                
                # 保存结果
                results.append({
                    "paper": paper_info,
                    "translation": result.choices[0].message.content
                })
                
                # 添加短暂延迟避免请求过快
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"处理论文时发生错误：{str(e)}")
                continue
            
        # 创建输出目录
        output_folder = 'HF-day-paper-deepseek'
        os.makedirs(output_folder, exist_ok=True)
        
        # 保存翻译结果
        output_file = os.path.join(output_folder, f"{yesterday_str}_HF_deepseek_clean.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        logger.info(f"翻译结果已保存到：{output_file}")
        
        # 生成海报
        create_poster(results, yesterday_str, output_folder)
        
        # 生成语音播报
        asyncio.run(generate_daily_paper_audio(yesterday_str))
        
        # 生成统计数据（分析最近7天的数据）
        end_date = yesterday_str
        start_date = (yesterday - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        analyze_papers(start_date, end_date)
        
        # 生成日报
        newsletter_generator = NewsletterGenerator()
        newsletter_generator.generate_newsletter(yesterday_str)
        
        logger.info("所有处理完成")
        
    except Exception as e:
        logger.error(f"处理论文时发生错误：{e}")
        raise  # 重新抛出异常以触发重试机制

if __name__ == "__main__":
    process_papers() 
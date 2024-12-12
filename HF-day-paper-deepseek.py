import os
import json
import re
import requests
from datetime import datetime, timedelta, timezone
from openai import OpenAI
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# 配置DeepSeek API
BASE_URL = "https://api.deepseek.com"
API_KEY = "sk-cea99987ce2248b4b1f77e876716f121"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# 获取当前UTC时间
current_utc_time = datetime.now(timezone.utc)
print(f"当前 UTC 日期和时间: {current_utc_time}")

# 将UTC时间转换为北京时间 (UTC+8)
beijing_timezone = timezone(timedelta(hours=8))
current_beijing_time = current_utc_time.astimezone(beijing_timezone)
print(f"当前北京时间和时间: {current_beijing_time}")

# 计算查询的日期(前一天)
yesterday_beijing = current_beijing_time - timedelta(days=1)
yesterday_str = yesterday_beijing.strftime('%Y-%m-%d')
print(f"查询的日期: {yesterday_str}")

# 搜索包含前一天日期的JSON文件
def find_files_with_date(search_path, date_str):
    result = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if date_str in file and file.endswith('.json'):
                result.append(os.path.join(root, file))
    return result

# 设置搜索路径为当前项目根目录
search_path = '.'

# 查找包含前一天日期的JSON文件
json_files = find_files_with_date(search_path, yesterday_str)
if not json_files:
    print(f'未找到包含前一天日期 "{yesterday_str}" 的JSON文件。')
else:
    print(f"找到以下文件：{json_files}")

# 矫正文件内容
def correct_json_content(data):
    if isinstance(data, list):
        # 将列表中的元素拼接成一个完整的字符串
        return ''.join(data)
    return data

# 提取ID并生成URL
def extract_ids(corrected_data):
    # 使用正则表达式提取ID
    ids = re.findall(r'\d{4}\.\d{5}', corrected_data)
    return ids

# 处理找到的JSON文件并保存结果
results = []

for file_path in json_files:
    print(f"找到文件：{file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            corrected_data = correct_json_content(data)
            print(f"矫正后的文件内容：\n{corrected_data}")
            
            # 提取ID并生成URL
            ids = extract_ids(corrected_data)
            # 使用tqdm显示进度条
            for arxiv_id in tqdm(ids, desc=f"Processing {file_path}", unit="id"):
                url = f"https://arxiv.org/abs/{arxiv_id}"
                print(f"Arxiv URL: {url}")
                
                # 调用DeepSeek API处理URL
                result = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that summarizes academic papers."
                        },
                        {
                            "role": "user",
                            "content": f"这篇文章的URL是：{url}。这篇文章讲了什么？"
                        }
                    ],
                    stream=False
                )
                
                # 输出调用结果
                print(result.choices[0].message.content)
                
                # 保存结果到列表中
                results.append({
                    "url": url,
                    "content": result.choices[0].message.content
                })
    except Exception as e:
        print(f"无法读取文件 {file_path}：{e}")

# 创建保存文件夹
output_folder = 'HF-day-paper-deepseek'
os.makedirs(output_folder, exist_ok=True)

# 保存结果到JSON文件
output_file = os.path.join(output_folder, f"{yesterday_str}_HF_deepseek_clean.json")
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print(f"结果已保存到文件：{output_file}")

def download_hf_icon():
    """下载 Hugging Face 图标"""
    icon_url = "https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png"
    response = requests.get(icon_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None

def create_rounded_rectangle(draw, xy, radius, fill):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill)  # 左上
    draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill)  # 右上
    draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill)  # 左下
    draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill)  # 右下
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)  # 中间矩形
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)  # 两侧矩形

def create_poster(results, date_str, output_folder):
    """创建每日论文总结海报"""
    # 设置海报尺寸和颜色
    width = 1200
    height = 1600
    
    # Hugging Face 品牌色系
    background_color = (247, 247, 248)  # 浅灰背景
    primary_color = (255, 172, 51)  # HF 黄色
    secondary_color = (48, 76, 125)  # HF 蓝色
    text_color = (0, 0, 0)  # 黑色文字
    card_color = (255, 255, 255)  # 白色卡片

    # 创建新图像
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    try:
        # 加载字体
        font_title = ImageFont.truetype("simhei.ttf", 60)
        font_subtitle = ImageFont.truetype("simhei.ttf", 40)
        font_content = ImageFont.truetype("simhei.ttf", 32)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_content = ImageFont.load_default()

    # 绘制顶部装饰条
    draw.rectangle([0, 0, width, 200], fill=primary_color)

    # 绘制标题
    title = "HF Daily Papers"
    draw.text((width//2, 100), title, font=font_title, fill=(255, 255, 255), anchor="mm")
    draw.text((width//2, 160), date_str, font=font_subtitle, fill=(255, 255, 255), anchor="mm")

    # 加载并放置 Hugging Face 图标
    try:
        icon = download_hf_icon()
        if icon:
            icon_size = 120
            icon = icon.resize((icon_size, icon_size))
            image.paste(icon, (50, 40), icon if icon.mode == 'RGBA' else None)
    except Exception as e:
        print(f"无法加载图标：{e}")

    # 绘制论文卡片
    y_position = 250
    for i, result in enumerate(results[:5], 1):
        # 创建卡片背景
        card_height = 250
        card_padding = 30
        create_rounded_rectangle(draw, 
                               [50, y_position, width-50, y_position+card_height],
                               20, card_color)

        # 绘制序号装饰
        number_circle_radius = 25
        circle_x = 80
        circle_y = y_position + 40
        draw.ellipse([circle_x-number_circle_radius, circle_y-number_circle_radius,
                     circle_x+number_circle_radius, circle_y+number_circle_radius],
                    fill=secondary_color)
        draw.text((circle_x, circle_y), str(i), font=font_subtitle, fill=(255, 255, 255), anchor="mm")

        # 提取arxiv ID
        arxiv_id = result['url'].split('/')[-1]
        
        # 绘制 arXiv ID
        draw.text((circle_x + 60, circle_y), f"arXiv:{arxiv_id}", 
                 font=font_subtitle, fill=secondary_color)

        # 绘制论文摘要
        content = result['content']
        # 文本换行处理
        words = list(content)
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(''.join(current_line)) >= 25:
                lines.append(''.join(current_line))
                current_line = []
        if current_line:
            lines.append(''.join(current_line))

        # 绘制摘要文本
        text_y = y_position + 100
        for line in lines[:3]:
            draw.text((80, text_y), line, font=font_content, fill=text_color)
            text_y += 40

        y_position += card_height + 30

    # 绘制底部装饰
    draw.rectangle([0, height-50, width, height], fill=primary_color)

    # 保存海报
    poster_path = os.path.join(output_folder, f"{date_str}_poster.png")
    image.save(poster_path)
    print(f"海报已保存到：{poster_path}")

# 生成海报
create_poster(results, yesterday_str, output_folder) 
import os
import json
import re
from datetime import datetime, timedelta
from openai import OpenAI
from tqdm import tqdm

# 配置OpenAI API
BASE_URL = os.getenv("OPENAI_API_BASE", "http://8.130.209.127:8000/v1")
API_KEY = "51d5350a075931c7.fa2eab916c0705fd6b120434ddd98e96"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# 获取当前日期并计算前一天的日期
current_date = datetime.now().date()
print(f"当前日期：{current_date}")

yesterday_date = current_date - timedelta(days=1)
print(f"前一天的日期：{yesterday_date}")

# 将前一天的日期转换为字符串格式
yesterday_str = yesterday_date.strftime('%Y-%m-%d')
print(f"前一天的日期字符串：{yesterday_str}")

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
    print(f"未找到包含前一天日期“{yesterday_str}”的JSON文件。")
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
                
                # 调用OpenAI API处理URL
                result = client.chat.completions.create(
                    model="660d7a0614c0acd012a10dc4",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"这篇文章的URL是：{url}。这篇文章讲了什么？"
                                }
                            ]
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

# 保存结果到JSON文件
output_file = f"{yesterday_str}_HF_glms_api_clean.json"
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print(f"结果已保存到文件：{output_file}")








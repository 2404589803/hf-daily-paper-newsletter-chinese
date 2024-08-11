import os
import json
import re
from datetime import datetime, timedelta, timezone
from zhipuai import ZhipuAI
from tqdm import tqdm

# 配置ZhipuAI API
API_KEY = "3db8a3bcecdae18ce765689c563fd2a6.qHjiJPELFaGCntzo"
client = ZhipuAI(api_key=API_KEY)

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
    print(f"未找到包含前一天日期“{yesterday_str}”的JSON文件。")
else:
    print(f"找到以下文件：{json_files}")

# 矫正文件内容
def correct_json_content(data):
    if isinstance(data, list):
        # 将列表中的元素拼接成一个完整的字符串
        return ''.join(data)
    return data

# 提取ID
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
            
            # 提取ID
            ids = extract_ids(corrected_data)
            # 使用tqdm显示进度条
            for arxiv_id in tqdm(ids, desc=f"Processing {file_path}", unit="id"):
                
                # 调用ZhipuAI API处理论文ID，获取论文的标题和摘要
                response = client.chat.completions.create(
                    model="glm-4",  # 替换为实际使用的模型名称
                    messages=[
                        {"role": "user", "content": f"论文ID为：{arxiv_id}。请提供论文的标题和摘要。"}
                    ],
                    stream=False
                )
                
                # 提取返回内容中的标题和摘要
                content = response.choices[0].delta
                title = re.search(r'标题:\s*(.*)', content)
                abstract = re.search(r'摘要:\s*(.*)', content)

                if title and abstract:
                    title_text = title.group(1)
                    abstract_text = abstract.group(1)

                    # 翻译摘要
                    translation_response = client.chat.completions.create(
                        model="glm-4",  # 替换为实际使用的模型名称
                        messages=[
                            {"role": "user", "content": f"请将以下英文摘要翻译成中文: {abstract_text}"}
                        ],
                        stream=False
                    )
                    translated_abstract = translation_response.choices[0].delta

                    # 保存结构化结果
                    results.append({
                        "title": title_text,
                        "arxiv_id": arxiv_id,
                        "abstract_cn": translated_abstract
                    })
    except Exception as e:
        print(f"无法读取文件 {file_path}：{e}")

# 创建保存文件夹
output_folder = 'HF-day-paper+GLMs-api'
os.makedirs(output_folder, exist_ok=True)

# 保存结果到JSON文件
output_file = os.path.join(output_folder, f"{yesterday_str}_HF_glms_api_clean.json")
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print(f"结果已保存到文件：{output_file}")


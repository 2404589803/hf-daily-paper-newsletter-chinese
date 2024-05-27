import os
import json
from datetime import datetime, timedelta
from zhipuai import ZhipuAI
from tqdm import tqdm

# 获取当天日期的前一天
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')

# 文件名假设为 "YYYY-MM-DD.json"
filename = f"{yesterday_str}.json"

# 搜索文件的根目录（可根据需要修改）
root_directory = '.'

# 搜索文件
file_path = None
for dirpath, dirnames, filenames in os.walk(root_directory):
    if filename in filenames:
        file_path = os.path.join(dirpath, filename)
        break

if file_path:
    # 读取JSON文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 将文件内容转换为字符串
    user_content = json.dumps(data, ensure_ascii=False)
else:
    user_content = f"文件 {filename} 不存在"

try:
    # 使用ZhipuAI客户端
    client = ZhipuAI(api_key="767b4fa4cdc4dfade85b100be96693fd.4E0Z62ttGa5nulIX")  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是一个论文结构化助手，你的任务是将user部分的其他无关内容去除，只输出每篇文章的题目的中文翻译和id"},
            {"role": "user", "content": user_content},
        ],
        stream=True,
    )

    # 初始化用于保存结果的列表
    structured_data = []

    # 处理响应并显示进度条
    print("正在处理响应...")
    for chunk in tqdm(response, desc="处理进度", unit="chunk"):
        delta_content = chunk.choices[0].delta
        if hasattr(delta_content, 'content'):
            # 提取 delta 中的内容并追加到结果列表中
            structured_data.append(delta_content.content)

    # 生成新的文件名
    clean_filename = f"{yesterday_str}_clean.json"

    # 将结构化数据写入新的JSON文件
    with open(clean_filename, 'w', encoding='utf-8') as clean_file:
        json.dump(structured_data, clean_file, ensure_ascii=False, indent=4)

    print(f"结构化数据已保存到 {clean_filename}")

except ValueError as e:
    print(f"发生错误: {e}")
except Exception as e:
    print(f"发生异常: {e}")







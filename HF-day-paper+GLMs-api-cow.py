import os
import json
import requests
from datetime import datetime, timedelta, timezone
import time
from tqdm import tqdm  # 导入tqdm模块

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

# 设置保存文件夹和文件路径
output_folder = 'HF-day-paper+GLMs-api'
output_file = os.path.join(output_folder, f"{yesterday_str}_HF_glms_api_clean.json")

# 检查文件是否存在
if not os.path.exists(output_file):
    print(f"未找到文件：{output_file}")
else:
    print(f"找到文件：{output_file}")

    # 读取文件内容
    with open(output_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # 检查读取的数据
    print(f"读取的数据类型: {type(data)}")
    print(f"读取的数据内容: {data}")

    # 设置请求的URL
    url = "http://8.130.209.127:5674/publish"

    # 发送POST请求
    headers = {'Content-Type': 'application/json'}
    print(f"发送请求到: {url}")
    
    # 如果data是一个字典列表，循环发送每个字典
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        for entry in tqdm(data, desc="发送进度", unit="entry"):
            print(f"发送条目: {json.dumps(entry, ensure_ascii=False, indent=4)}")
            try:
                response = requests.post(url, headers=headers, json=entry)
                # 检查响应
                if response.status_code == 200:
                    print(f"请求成功: {response.json()}")
                elif response.status_code == 422:
                    print(f"无法处理的实体: 状态码 {response.status_code}，响应内容: {response.text}")
                else:
                    print(f"请求失败: 状态码 {response.status_code}，响应内容: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"请求异常: {e}")

            # 发送完一个条目后，等待5分钟（300秒）
            print("等待5分钟...")
            for i in tqdm(range(300), desc="等待时间", unit="秒"):
                time.sleep(1)
    else:
        print("数据格式不符合预期，请检查数据格式是否为字典列表。")










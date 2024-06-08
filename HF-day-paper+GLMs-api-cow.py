import os
import json
import requests
from datetime import datetime, timedelta, timezone

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

    # 设置请求的URL
    url = "http://8.130.209.127:5674/publish"

    # 发送POST请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)

    # 检查响应
    if response.status_code == 200:
        print(f"请求成功: {response.json()}")
    else:
        print(f"请求失败: 状态码 {response.status_code}，响应内容: {response.text}")

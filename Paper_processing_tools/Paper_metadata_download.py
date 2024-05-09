import requests
from datetime import datetime, timedelta
import os

# 指定保存数据的文件夹路径
save_folder = "D:\\python project\\hf-daily-paper-newsletter-chinese\\daily_papers"

# 创建保存数据的文件夹（如果不存在）
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 获取当前日期
current_date = datetime.now()

# 计算查询的日期(前一天)
query_date = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')

# 构建API URL
url = f"https://huggingface.co/api/daily_papers?date={query_date}"

# 发送GET请求
response = requests.get(url)

if response.status_code == 200:
    # 检查是否有数据
    if response.json():
        # 如果返回的不是空列表
        # 构建文件路径
        file_path = os.path.join(save_folder, f'daily_papers_{query_date}.json')
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"在 {query_date} 找到数据，已下载完成，保存在 {file_path}")
    else:
        print(f"在 {query_date} 没有找到数据")
else:
    print(f"请求失败，状态码：{response.status_code}")
    print(response.json())  # 打印出详细的错误信息
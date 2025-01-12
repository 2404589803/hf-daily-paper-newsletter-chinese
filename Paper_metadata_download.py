import unittest
import requests
from datetime import datetime, timedelta, timezone
import json
import os

def download_papers(date_str=None):
    """下载指定日期的论文数据"""
    # 如果没有指定日期，使用昨天的日期
    if not date_str:
        # 获取当前日期和时间 (UTC 时间)
        current_date = datetime.now(timezone.utc)
        # 将 UTC 时间转换为北京时间 (UTC+8)
        beijing_timezone = timezone(timedelta(hours=8))
        current_date_beijing = current_date.astimezone(beijing_timezone)
        # 计算查询的日期(前一天)
        date_str = (current_date_beijing - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # 构建API URL
    url = f"https://huggingface.co/api/daily_papers?date={date_str}"
    print(f"正在获取 {date_str} 的论文数据...")
    print(f"API URL: {url}")
    
    # 定义文件夹和文件名
    folder_name = 'Paper_metadata_download'
    file_name = f"{date_str}.json"
    
    # 创建文件夹（如果不存在）
    os.makedirs(folder_name, exist_ok=True)
    
    # 完整文件路径
    file_path = os.path.join(folder_name, file_name)
    
    try:
        # 检查是否已经下载过该日期的数据
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                if isinstance(existing_data, dict) and existing_data.get("status") == "success":
                    print(f"已存在 {date_str} 的有效数据，跳过下载")
                    return existing_data
        
        # 发送GET请求
        response = requests.get(url)
        
        if response.status_code == 200:
            # 检查是否有数据
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                # 如果返回的不是空列表
                print(f"在 {date_str} 找到 {len(data)} 篇论文")
                # 将数据写入JSON文件
                result = {
                    "status": "success",
                    "date": date_str,
                    "count": len(data),
                    "data": [str(paper) for paper in data]  # 将每个paper对象转换为字符串
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                print(f"数据已写入文件 {file_path}")
                return result
            else:
                print(f"在 {date_str} 没有找到论文数据")
                # 写入空数据标记到文件
                result = {
                    "status": "no_data",
                    "date": date_str,
                    "message": "No papers found for this date"
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                return result
        else:
            print(f"请求失败，状态码：{response.status_code}")
            print(response.text)  # 打印出详细的错误信息
            result = {
                "status": "error",
                "date": date_str,
                "code": response.status_code,
                "message": response.text
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            return result
    except Exception as e:
        print(f"处理数据时发生异常: {e}")
        result = {
            "status": "error",
            "date": date_str,
            "message": str(e)
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result

def find_latest_data(max_days=7):
    """查找最近有数据的日期"""
    current_date = datetime.now(timezone.utc)
    beijing_timezone = timezone(timedelta(hours=8))
    current_date_beijing = current_date.astimezone(beijing_timezone)
    
    for i in range(max_days):
        date_str = (current_date_beijing - timedelta(days=i)).strftime('%Y-%m-%d')
        result = download_papers(date_str)
        if result.get("status") == "success" and result.get("count", 0) > 0:
            return date_str, result
    return None, None

class TestDailyPapers(unittest.TestCase):
    def test_download_papers(self):
        """测试论文下载功能"""
        # 使用当前日期进行测试
        result = download_papers()
        self.assertTrue(result)

if __name__ == '__main__':
    # 如果直接运行脚本，则下载论文
    if os.environ.get('RUNNING_TESTS') == 'true':
        unittest.main(exit=False)
    else:
        # 先尝试下载昨天的数据
        result = download_papers()
        if result.get("status") != "success" or result.get("count", 0) == 0:
            # 如果昨天没有数据，查找最近有数据的日期
            latest_date, latest_data = find_latest_data()
            if latest_date:
                print(f"找到最近的数据日期：{latest_date}，共 {latest_data.get('count')} 篇论文")
            else:
                print("在最近7天内未找到任何论文数据")







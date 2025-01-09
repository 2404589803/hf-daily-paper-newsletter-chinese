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
    
    # 发送GET请求
    response = requests.get(url)
    
    # 定义文件夹和文件名
    folder_name = 'Paper_metadata_download'
    file_name = f"{date_str}.json"
    
    # 创建文件夹（如果不存在）
    os.makedirs(folder_name, exist_ok=True)
    
    # 完整文件路径
    file_path = os.path.join(folder_name, file_name)
    
    try:
        if response.status_code == 200:
            # 检查是否有数据
            data = response.json()
            if data:
                # 如果返回的不是空列表
                print(f"在 {date_str} 找到数据")
                # 将数据写入JSON文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    papers_str = [str(paper) for paper in data]  # 将每个paper对象转换为字符串
                    json.dump(papers_str, f, ensure_ascii=False, indent=4)
                print(f"数据已写入文件 {file_path}")
                return True
            else:
                print(f"在 {date_str} 没有找到数据")
                # 写入1到文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(1, f)
                print(f"1 已写入文件 {file_path}")
                return True
        else:
            print(f"请求失败，状态码：{response.status_code}")
            print(response.text)  # 打印出详细的错误信息
            return False
    except Exception as e:
        print(f"处理数据时发生异常: {e}")
        return False

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
        download_papers()







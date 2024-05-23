import unittest
import requests
from datetime import datetime, timedelta

class TestDailyPapers(unittest.TestCase):

    def setUp(self):
        # 获取当前日期
        self.current_date = datetime.now()

        # 计算查询的日期(前一天)
        self.query_date = (self.current_date - timedelta(days=1)).strftime('%Y-%m-%d')

        # 构建API URL
        self.url = f"https://huggingface.co/api/daily_papers?date={self.query_date}"

    def test_get_daily_papers(self):
        # 发送GET请求
        response = requests.get(self.url)

        if response.status_code == 200:
            # 检查是否有数据
            data = response.json()
            if data:
                # 如果返回的不是空列表
                print(f"在 {self.query_date} 找到数据:")
                print(data)
                self.assertTrue(True)
            else:
                print(f"在 {self.query_date} 没有找到数据")
                self.assertTrue(False)
        else:
            print(f"请求失败，状态码：{response.status_code}")
            print(response.json())  # 打印出详细的错误信息
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()


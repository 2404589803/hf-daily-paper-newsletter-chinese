import unittest
import os
import requests
from datetime import datetime, timedelta

class TestDailyPapers(unittest.TestCase):

    def setUp(self):
        # 指定保存数据的文件夹路径，使用相对于 GitHub Actions 工作区的路径
        self.save_folder = "${{ github.workspace }}/daily_papers"

        # 创建保存数据的文件夹（如果不存在）
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

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
            if response.json():
                # 如果返回的不是空列表
                # 构建文件路径
                file_path = os.path.join(self.save_folder, f'daily_papers_{self.query_date}.json')

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                self.assertTrue(os.path.exists(file_path))
                print(f"在 {self.query_date} 找到数据，已下载完成，保存在 {file_path}")
            else:
                print(f"在 {self.query_date} 没有找到数据")
        else:
            print(f"请求失败，状态码：{response.status_code}")
            print(response.json())  # 打印出详细的错误信息

if __name__ == '__main__':
    unittest.main()

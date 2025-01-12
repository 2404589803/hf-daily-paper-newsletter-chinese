import os
import json
import datetime
import pytz
import requests
import logging
from utils import setup_logger

# 设置日志记录器
logger = setup_logger()

def download_papers():
    """下载论文数据"""
    try:
        # 获取当天的日期
        beijing_tz = pytz.timezone('Asia/Shanghai')
        current_time = datetime.datetime.now(beijing_tz)
        date_str = current_time.strftime('%Y-%m-%d')
        
        logger.info(f"正在获取 {date_str} 的论文数据")
        
        # 构建API URL
        url = f"https://huggingface.co/api/papers/daily/{date_str}"
        
        # 发送请求
        response = requests.get(url)
        
        # 检查响应状态
        if response.status_code == 200:
            papers = response.json()
            if papers:
                # 创建输出目录
                os.makedirs('Paper_metadata_download', exist_ok=True)
                output_file = os.path.join('Paper_metadata_download', f"{date_str}.json")
                
                # 保存数据
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(papers, f, ensure_ascii=False, indent=2)
                logger.info(f"成功下载并保存了 {len(papers)} 篇论文的数据")
                return {"status": "success", "date": date_str}
            else:
                logger.warning(f"{date_str} 没有可用的论文数据")
                return {"status": "no_data", "date": date_str}
        else:
            logger.error(f"API请求失败: {response.status_code}")
            return {"status": "error", "date": date_str, "message": f"API请求失败: {response.status_code}"}
            
    except Exception as e:
        logger.error(f"下载论文数据时发生错误: {str(e)}")
        return {"status": "error", "date": date_str, "message": str(e)}

if __name__ == "__main__":
    result = download_papers()
    logger.info(f"下载结果: {result}")
    if result["status"] != "success":
        exit(1)







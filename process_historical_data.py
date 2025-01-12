import sys
import os
from datetime import datetime, timedelta
import json
from Paper_metadata_download import download_papers
from HF_day_paper_deepseek import process_papers
from newsletter import generate_newsletter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_date(date_str):
    """处理指定日期的数据"""
    try:
        # 下载该日期的论文数据
        logger.info(f"Processing date: {date_str}")
        json_file = f"Paper_metadata_download/{date_str}.json"
        
        # 如果文件已存在且大小大于1字节，跳过下载
        if os.path.exists(json_file) and os.path.getsize(json_file) > 1:
            logger.info(f"File {json_file} already exists and is valid")
        else:
            logger.info(f"Downloading papers for {date_str}")
            download_papers(date_str)
        
        # 检查文件是否存在且有效
        if not os.path.exists(json_file) or os.path.getsize(json_file) <= 1:
            logger.warning(f"No valid data found for {date_str}")
            return False
            
        # 处理论文数据
        logger.info(f"Processing papers for {date_str}")
        process_papers(date_str)
        
        # 生成newsletter
        logger.info(f"Generating newsletter for {date_str}")
        generate_newsletter(date_str)
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing {date_str}: {str(e)}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python process_historical_data.py start_date end_date")
        print("Example: python process_historical_data.py 2024-01-01 2024-01-31")
        sys.exit(1)
        
    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        process_date(date_str)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main() 
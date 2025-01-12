import os
import glob
from datetime import datetime
import json
from Paper_metadata_download import download_papers
import importlib.util
import sys

# 动态导入带横线的模块
def import_dash_module(file_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# 导入模块
hf_paper = import_dash_module("HF-day-paper-deepseek.py", "hf_paper")
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
        
        # 检查文件是否存在且有效
        if not os.path.exists(json_file) or os.path.getsize(json_file) <= 1:
            logger.warning(f"No valid data found for {date_str}")
            return False
            
        # 处理论文数据
        logger.info(f"Processing papers for {date_str}")
        hf_paper.process_papers(date_str)
        
        # 生成newsletter
        logger.info(f"Generating newsletter for {date_str}")
        generate_newsletter(date_str)
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing {date_str}: {str(e)}")
        return False

def get_existing_dates():
    """获取Paper_metadata_download目录下所有有效的数据文件日期"""
    data_files = glob.glob("Paper_metadata_download/*.json")
    valid_dates = []
    
    for file_path in data_files:
        # 检查文件大小是否大于1字节
        if os.path.getsize(file_path) > 1:
            # 从文件名中提取日期
            date_str = os.path.basename(file_path).replace(".json", "")
            try:
                # 验证日期格式
                datetime.strptime(date_str, "%Y-%m-%d")
                valid_dates.append(date_str)
            except ValueError:
                continue
    
    return sorted(valid_dates)

def main():
    # 获取所有有效的数据文件日期
    dates = get_existing_dates()
    
    if not dates:
        logger.warning("No valid data files found in Paper_metadata_download directory")
        return
    
    logger.info(f"Found {len(dates)} valid data files")
    logger.info(f"Date range: from {dates[0]} to {dates[-1]}")
    
    # 处理每个日期的数据
    for date_str in dates:
        process_date(date_str)

if __name__ == "__main__":
    main() 
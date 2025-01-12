import os
import glob
from datetime import datetime
import json
from Paper_metadata_download import download_papers
import importlib.util
import sys
import traceback

# 动态导入带横线的模块
def import_dash_module(file_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# 导入模块
hf_paper = import_dash_module("HF-day-paper-deepseek.py", "hf_paper")
from newsletter import NewsletterGenerator
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
            
        # 读取JSON文件
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                papers_data = json.load(f)
            logger.info(f"Successfully loaded {len(papers_data)} papers from {json_file}")
        except Exception as e:
            logger.error(f"Error loading {json_file}: {str(e)}")
            return False
            
        # 处理论文数据
        logger.info(f"Processing papers for {date_str}")
        try:
            # 设置日期环境变量
            os.environ['PROCESS_DATE'] = date_str
            hf_paper.process_papers()
            # 清理环境变量
            del os.environ['PROCESS_DATE']
        except Exception as e:
            logger.error(f"Error in process_papers for {date_str}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        # 生成newsletter
        logger.info(f"Generating newsletter for {date_str}")
        try:
            newsletter_generator = NewsletterGenerator()
            newsletter_generator.generate_newsletter(date_str)
        except Exception as e:
            logger.error(f"Error generating newsletter for {date_str}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing {date_str}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def get_existing_dates():
    """获取Paper_metadata_download目录下所有有效的数据文件日期"""
    data_files = glob.glob("Paper_metadata_download/*.json")
    valid_dates = []
    
    for file_path in data_files:
        try:
            # 检查文件大小是否大于1字节
            if os.path.getsize(file_path) > 1:
                # 从文件名中提取日期
                date_str = os.path.basename(file_path).replace(".json", "")
                try:
                    # 验证日期格式
                    datetime.strptime(date_str, "%Y-%m-%d")
                    # 检查JSON文件是否有效
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list) and len(data) > 0:
                            valid_dates.append(date_str)
                        else:
                            logger.warning(f"File {file_path} has invalid data structure")
                except ValueError:
                    logger.warning(f"Invalid date format in filename: {file_path}")
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON file: {file_path}")
                except Exception as e:
                    logger.warning(f"Error processing file {file_path}: {str(e)}")
        except Exception as e:
            logger.warning(f"Error checking file {file_path}: {str(e)}")
    
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
    success_count = 0
    error_count = 0
    for date_str in dates:
        if process_date(date_str):
            success_count += 1
        else:
            error_count += 1
            
    logger.info(f"Processing completed. Success: {success_count}, Error: {error_count}")

if __name__ == "__main__":
    main() 
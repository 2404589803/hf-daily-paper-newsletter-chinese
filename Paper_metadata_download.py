import os
import json
import datetime
import pytz
import requests
import logging
import argparse
from utils import setup_logger

# 设置日志记录器
logger = setup_logger()

def download_papers(date_str=None):
    """
    下载论文数据
    Args:
        date_str: 可选，指定要下载的日期，格式为YYYY-MM-DD。如果不指定，则使用当前日期。
    """
    try:
        # 如果没有指定日期，使用北京时间当前日期
        if date_str is None:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            current_time = datetime.datetime.now(beijing_tz)
            date_str = current_time.strftime('%Y-%m-%d')
        
        logger.info(f"正在获取 {date_str} 的论文数据")
        
        # 构建API URL
        url = f"https://huggingface.co/api/daily_papers?date={date_str}"
        
        # 发送请求
        response = requests.get(url)
        
        # 检查响应状态
        if response.status_code == 200:
            papers = response.json()
            logger.info(f"API返回原始数据数量: {len(papers)}")
            
            if papers:
                # 过滤有效的论文数据
                valid_papers = []
                skipped_papers = []
                
                for paper in papers:
                    paper_info = paper.get('paper', {})
                    paper_id = paper_info.get('id', 'unknown')
                    
                    # 详细的验证逻辑
                    is_valid = True
                    reasons = []
                    
                    if not paper_info:
                        is_valid = False
                        reasons.append("缺少paper字段")
                    else:
                        if not paper_info.get('title'):
                            is_valid = False
                            reasons.append("缺少标题")
                        if not paper_info.get('summary'):
                            is_valid = False
                            reasons.append("缺少摘要")
                        if not paper_info.get('id'):
                            is_valid = False
                            reasons.append("缺少ID")
                        if not paper_info.get('authors'):
                            is_valid = False
                            reasons.append("缺少作者信息")
                        if not paper.get('publishedAt'):
                            is_valid = False
                            reasons.append("缺少发布时间")
                    
                    if is_valid:
                        valid_papers.append(paper)
                        logger.debug(f"接受论文: {paper_id}")
                    else:
                        skipped_papers.append({
                            'id': paper_id,
                            'reasons': reasons
                        })
                        logger.warning(f"跳过论文 {paper_id}: {', '.join(reasons)}")
                
                logger.info(f"原始数据: {len(papers)}篇")
                logger.info(f"有效论文: {len(valid_papers)}篇")
                logger.info(f"跳过论文: {len(skipped_papers)}篇")
                
                if skipped_papers:
                    logger.info("跳过的论文详情:")
                    for skip_info in skipped_papers:
                        logger.info(f"  ID: {skip_info['id']}, 原因: {', '.join(skip_info['reasons'])}")
                
                if valid_papers:
                    # 只在有数据时创建文件
                    os.makedirs('Paper_metadata_download', exist_ok=True)
                    output_file = os.path.join('Paper_metadata_download', f"{date_str}.json")
                    
                    # 保存数据
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(valid_papers, f, ensure_ascii=False, indent=2)
                    logger.info(f"成功保存 {len(valid_papers)} 篇有效论文数据到文件")
                    return {"status": "success", "date": date_str}
                else:
                    logger.warning(f"{date_str} 没有有效的论文数据")
                    return {"status": "no_data", "date": date_str}
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
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='下载HuggingFace每日论文数据')
    parser.add_argument('--date', type=str, help='指定要下载的日期 (YYYY-MM-DD格式)')
    args = parser.parse_args()

    # 使用指定的日期或默认使用当前日期
    result = download_papers(args.date)
    logger.info(f"下载结果: {result}")
    # 只有在发生错误时才返回非零状态码
    if result["status"] == "error":
        exit(1)
    # 没有数据时返回状态码 0
    exit(0)







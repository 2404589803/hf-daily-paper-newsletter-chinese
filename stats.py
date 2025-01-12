import json
import os
from collections import Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
import numpy as np
import re
from utils import get_logger

logger = get_logger()

# 中文停用词列表
STOPWORDS = {'的', '了', '和', '是', '在', '我们', '通过', '使用', '基于', '提出', '本文', '一个', '方法', '进行', '可以', '以及', '等', '与', '该', '这个', '为', '并', '对', '从', '将', '同时', '或', '由', '及', '上', '中', '下', '等等', '更', '能', '都', '把', '被', '比', '这', '那', '有', '就', '而', '且', '但', '并且', '或者', '不', '也', '还', '个', '之', '于', '这些', '这样', '一些', '一种', '这种', '另', '另外', '另一', '可能', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十'}

def analyze_papers(start_date=None, end_date=None):
    """分析指定日期范围内的论文数据"""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
        
    logger.info(f"开始分析论文数据，时间范围：{start_date} 至 {end_date}")
        
    stats = {
        'total_papers': 0,
        'keywords': Counter(),
        'daily_counts': {},
        'titles': []
    }
    
    # 创建统计结果目录
    os.makedirs('stats', exist_ok=True)
    
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    has_valid_data = False
    
    while current_date <= end:
        date_str = current_date.strftime('%Y-%m-%d')
        file_path = os.path.join('HF-day-paper-deepseek', f"{date_str}_HF_deepseek_clean.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 检查是否是有效的数据文件
                if isinstance(data, list) and len(data) > 0:
                    daily_count = len(data)
                    stats['total_papers'] += daily_count
                    stats['daily_counts'][date_str] = daily_count
                    has_valid_data = True
                    logger.info(f"处理 {date_str} 的数据：找到 {daily_count} 篇论文")
                    
                    # 分析论文内容
                    for paper in data:
                        translation = paper.get('translation', '')
                        # 提取中文关键词
                        words = jieba.cut(translation)
                        # 过滤停用词、单个字符和数字
                        keywords = [w for w in words if len(w) > 1 and not w.isspace() and w not in STOPWORDS and not w.isdigit()]
                        stats['keywords'].update(keywords)
                        
                        # 保存标题
                        title_match = re.search(r"标题[:：](.*?)(?=\n摘要[:：]|\Z)", translation, re.DOTALL)
                        if title_match:
                            title = title_match.group(1).strip()
                            stats['titles'].append(title)
                else:
                    logger.info(f"跳过 {date_str} 的数据：无有效论文")
                        
            except Exception as e:
                logger.error(f"处理 {date_str} 的数据时出错：{str(e)}")
                
        current_date += timedelta(days=1)
    
    if not has_valid_data:
        logger.warning("在指定时间范围内未找到任何有效的论文数据")
        return None
    
    # 生成统计图表
    try:
        if stats['daily_counts']:
            generate_stats_visualizations(stats, start_date, end_date)
            logger.info("统计图表生成完成")
            
            # 保存统计结果
            report = {
                'period': f"{start_date} 至 {end_date}",
                'total_papers': stats['total_papers'],
                'daily_average': round(stats['total_papers'] / len(stats['daily_counts']), 2),
                'top_keywords': dict(stats['keywords'].most_common(20)),
                'daily_counts': stats['daily_counts']
            }
            
            # 创建统计数据目录
            stats_dir = 'stats'
            os.makedirs(stats_dir, exist_ok=True)
            with open(os.path.join(stats_dir, 'stats_report.json'), 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=4)
                
            return stats
    except Exception as e:
        logger.error(f"生成统计图表时出错：{str(e)}")
        return None

def generate_stats_visualizations(stats, start_date, end_date):
    """生成统计可视化图表"""
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei'] if os.name != 'nt' else ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图片输出目录
    images_dir = 'images'
    os.makedirs(images_dir, exist_ok=True)
    
    # 生成每日论文数量折线图
    plt.figure(figsize=(12, 6))
    dates = list(stats['daily_counts'].keys())
    counts = list(stats['daily_counts'].values())
    plt.plot(dates, counts, marker='o', linewidth=2, markersize=8)
    plt.title(f'每日论文数量统计 ({start_date} 至 {end_date})', fontsize=14, pad=20)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('论文数量', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'daily_papers.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 生成关键词词云
    if stats['keywords']:
        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='white',
            font_path='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc' if os.name != 'nt' else 'C:\\Windows\\Fonts\\msyh.ttc',
            max_words=100,
            min_font_size=10,
            max_font_size=120,
            random_state=42
        )
        wordcloud.generate_from_frequencies(dict(stats['keywords'].most_common(100)))
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('论文关键词云图', fontsize=16, pad=20)
        plt.savefig(os.path.join(images_dir, 'keywords_wordcloud.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 保存统计结果
    report = {
        'period': f"{start_date} 至 {end_date}",
        'total_papers': stats['total_papers'],
        'daily_average': round(stats['total_papers'] / len(stats['daily_counts']), 2),
        'top_keywords': dict(stats['keywords'].most_common(20)),
        'daily_counts': stats['daily_counts']
    }
    
    # 创建统计数据目录
    stats_dir = 'stats'
    os.makedirs(stats_dir, exist_ok=True)
    with open(os.path.join(stats_dir, 'stats_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4) 
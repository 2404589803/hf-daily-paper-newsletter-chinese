import json
import os
from collections import Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
import numpy as np
import re
import argparse
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
    
    # 创建统计结果目录
    stats_dir = 'stats'
    os.makedirs(stats_dir, exist_ok=True)
    
    # 初始化新的统计数据
    stats = {
        'total_papers': 0,
        'keywords': Counter(),
        'daily_counts': {},
        'titles': []
    }
    
    # 如果是处理单日数据，不需要读取现有统计
    is_single_day = start_date == end_date
    if not is_single_day:
        # 尝试读取现有的统计数据
        stats_file = os.path.join(stats_dir, 'stats_report.json')
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    existing_stats = json.load(f)
                    stats = {
                        'total_papers': existing_stats.get('total_papers', 0),
                        'keywords': Counter(existing_stats.get('top_keywords', {})),
                        'daily_counts': existing_stats.get('daily_counts', {}),
                        'titles': existing_stats.get('titles', [])
                    }
            except Exception as e:
                logger.error(f"读取现有统计数据时出错：{str(e)}")
    
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    has_valid_data = False
    new_data_processed = False
    
    while current_date <= end:
        date_str = current_date.strftime('%Y-%m-%d')
        # 如果是单日处理或者这一天的数据不存在于统计中，则处理
        if is_single_day or date_str not in stats['daily_counts']:
            file_path = os.path.join('HF-day-paper-deepseek', f"{date_str}_HF_deepseek_clean.json")
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # 检查是否是有效的数据文件
                    if isinstance(data, list) and len(data) > 0:
                        daily_count = len(data)
                        if is_single_day:
                            # 单日处理时重置计数
                            stats['total_papers'] = daily_count
                            stats['daily_counts'] = {date_str: daily_count}
                        else:
                            stats['total_papers'] += daily_count
                            stats['daily_counts'][date_str] = daily_count
                        
                        has_valid_data = True
                        new_data_processed = True
                        logger.info(f"处理 {date_str} 的数据：找到 {daily_count} 篇论文")
                        
                        # 分析论文内容
                        for paper in data:
                            translation = paper.get('translation', '')
                            # 提取中文关键词
                            words = jieba.cut(translation)
                            # 过滤停用词、单个字符和数字
                            keywords = [w for w in words if len(w) > 1 and not w.isspace() and w not in STOPWORDS and not w.isdigit()]
                            if is_single_day:
                                # 单日处理时使用新的关键词计数器
                                stats['keywords'] = Counter(keywords)
                            else:
                                stats['keywords'].update(keywords)
                            
                            # 保存标题
                            title_match = re.search(r"标题[:：](.*?)(?=\n摘要[:：]|\Z)", translation, re.DOTALL)
                            if title_match:
                                title = title_match.group(1).strip()
                                if is_single_day:
                                    # 单日处理时重置标题列表
                                    if title not in stats['titles']:
                                        stats['titles'] = [title]
                                else:
                                    if title not in stats['titles']:
                                        stats['titles'].append(title)
                    else:
                        logger.info(f"跳过 {date_str} 的数据：无有效论文")
                            
                except Exception as e:
                    logger.error(f"处理 {date_str} 的数据时出错：{str(e)}")
                    
        current_date += timedelta(days=1)
    
    if not has_valid_data and not stats['daily_counts']:
        logger.warning("在指定时间范围内未找到任何有效的论文数据")
        return None
    
    # 只有在处理了新数据时才更新统计图表
    if new_data_processed:
        try:
            if stats['daily_counts']:
                generate_stats_visualizations(stats, min(stats['daily_counts'].keys()), max(stats['daily_counts'].keys()))
                logger.info("统计图表生成完成")
                
                # 保存统计结果
                report = {
                    'period': f"{min(stats['daily_counts'].keys())} 至 {max(stats['daily_counts'].keys())}",
                    'total_papers': stats['total_papers'],
                    'daily_average': round(stats['total_papers'] / len(stats['daily_counts']), 2),
                    'top_keywords': dict(stats['keywords'].most_common(20)),
                    'daily_counts': dict(sorted(stats['daily_counts'].items())),  # 按日期排序
                    'titles': stats['titles']
                }
                
                with open(os.path.join(stats_dir, 'stats_report.json'), 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=4)
                    
                return stats
        except Exception as e:
            logger.error(f"生成统计图表时出错：{str(e)}")
            return None
    
    return stats

def generate_stats_visualizations(stats, start_date, end_date):
    """生成统计可视化图表"""
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Zenhei', 'Noto Sans CJK JP']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图片输出目录
    images_dir = 'images'
    os.makedirs(images_dir, exist_ok=True)
    
    # 判断是否是单日数据
    is_single_day = start_date == end_date
    
    # 生成每日论文数量折线图
    plt.figure(figsize=(12, 6))
    
    # 对日期进行排序
    sorted_dates = sorted(stats['daily_counts'].keys())
    sorted_counts = [stats['daily_counts'][date] for date in sorted_dates]
    
    # 计算累积数量
    cumulative_counts = np.cumsum(sorted_counts)
    
    if is_single_day:
        # 单日数据时只显示一个图表
        plt.figure(figsize=(15, 6))
        plt.bar(sorted_dates, sorted_counts, color=plt.cm.Set3(0), label='论文数量')
        plt.title(f'论文数量统计 ({start_date})', fontsize=14, pad=20)
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('论文数量', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'daily_papers.png'), dpi=300, bbox_inches='tight')
        plt.close()
    else:
        # 多日数据时显示两个子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), height_ratios=[1, 1])
        
        # 绘制每日论文数量
        ax1.plot(sorted_dates, sorted_counts, marker='o', linewidth=2, markersize=8, label='每日论文数量')
        ax1.set_title(f'每日论文数量统计 ({start_date} 至 {end_date})', fontsize=14, pad=20)
        ax1.set_xlabel('日期', fontsize=12)
        ax1.set_ylabel('论文数量', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend()
        
        # 绘制累积论文数量
        ax2.plot(sorted_dates, cumulative_counts, marker='s', linewidth=2, markersize=8, color='orange', label='累积论文数量')
        ax2.set_title('累积论文数量统计', fontsize=14, pad=20)
        ax2.set_xlabel('日期', fontsize=12)
        ax2.set_ylabel('累积数量', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'daily_papers.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 生成关键词词云
    if stats['keywords']:
        # 创建词云图
        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='white',
            font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc' if os.name != 'nt' else 'C:\\Windows\\Fonts\\msyh.ttc',
            max_words=100,
            min_font_size=10,
            max_font_size=120,
            random_state=42
        )
        wordcloud.generate_from_frequencies(dict(stats['keywords'].most_common(100)))
        
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        if is_single_day:
            plt.title(f'{start_date} 关键词云图', fontsize=16, pad=20)
        else:
            plt.title(f'{start_date} 至 {end_date} 关键词云图', fontsize=16, pad=20)
        
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'keywords_wordcloud.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 保存统计结果
    report = {
        'period': f"{start_date} 至 {end_date}",
        'total_papers': stats['total_papers'],
        'daily_average': round(stats['total_papers'] / len(stats['daily_counts']), 2),
        'top_keywords': dict(stats['keywords'].most_common(20)),
        'daily_counts': dict(sorted(stats['daily_counts'].items())),  # 按日期排序
        'titles': stats['titles']
    }
    
    # 创建统计数据目录
    stats_dir = 'stats'
    os.makedirs(stats_dir, exist_ok=True)
    with open(os.path.join(stats_dir, 'stats_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='分析HuggingFace每日论文数据')
    parser.add_argument('--start-date', type=str, help='分析开始日期 (YYYY-MM-DD格式)')
    parser.add_argument('--end-date', type=str, help='分析结束日期 (YYYY-MM-DD格式)')
    args = parser.parse_args()

    # 使用指定的日期范围或默认使用最近7天
    stats = analyze_papers(args.start_date, args.end_date)
    if not stats:
        exit(1)
    exit(0) 
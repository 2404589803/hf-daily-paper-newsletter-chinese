import json
import os
from collections import Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
import numpy as np

def analyze_papers(start_date=None, end_date=None):
    """分析指定日期范围内的论文数据"""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
        
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
    
    while current_date <= end:
        date_str = current_date.strftime('%Y-%m-%d')
        file_path = os.path.join('HF-day-paper-deepseek', f"{date_str}_HF_deepseek_clean.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                daily_count = len(data)
                stats['total_papers'] += daily_count
                stats['daily_counts'][date_str] = daily_count
                
                # 分析论文内容
                for paper in data:
                    translation = paper.get('translation', '')
                    # 提取中文关键词
                    words = jieba.cut(translation)
                    # 过滤停用词和单个字符
                    keywords = [w for w in words if len(w) > 1 and not w.isspace()]
                    stats['keywords'].update(keywords)
                    
                    # 保存标题
                    if '标题：' in translation:
                        title = translation.split('标题：')[1].split('\n')[0]
                        stats['titles'].append(title)
                        
            except Exception as e:
                print(f"处理{date_str}的数据时出错：{str(e)}")
                
        current_date += timedelta(days=1)
    
    # 生成统计图表
    generate_stats_visualizations(stats, start_date, end_date)
    
    return stats

def generate_stats_visualizations(stats, start_date, end_date):
    """生成统计可视化图表"""
    # 生成每日论文数量折线图
    plt.figure(figsize=(12, 6))
    dates = list(stats['daily_counts'].keys())
    counts = list(stats['daily_counts'].values())
    plt.plot(dates, counts, marker='o')
    plt.title(f'每日论文数量统计 ({start_date} 至 {end_date})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join('stats', 'daily_papers.png'))
    plt.close()
    
    # 生成关键词词云
    wordcloud = WordCloud(
        width=1200,
        height=800,
        background_color='white',
        font_path='C:\\Windows\\Fonts\\msyh.ttc' if os.name == 'nt' else '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
    )
    wordcloud.generate_from_frequencies(dict(stats['keywords'].most_common(100)))
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(os.path.join('stats', 'keywords_wordcloud.png'))
    plt.close()
    
    # 保存统计结果
    report = {
        'period': f"{start_date} 至 {end_date}",
        'total_papers': stats['total_papers'],
        'daily_average': round(stats['total_papers'] / len(stats['daily_counts']), 2),
        'top_keywords': dict(stats['keywords'].most_common(20)),
        'daily_counts': stats['daily_counts']
    }
    
    with open(os.path.join('stats', 'stats_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4) 
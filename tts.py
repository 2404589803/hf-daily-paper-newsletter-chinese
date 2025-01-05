import os
import json
from datetime import datetime
import edge_tts
import asyncio
from utils import get_logger

logger = get_logger()

async def generate_audio(text, output_path):
    """使用 Edge TTS 生成语音"""
    try:
        voice = "zh-CN-XiaoxiaoNeural"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return True
    except Exception as e:
        logger.error(f"生成语音时出错：{str(e)}")
        return False

async def generate_daily_paper_audio(date_str=None):
    """为指定日期的论文生成语音播报"""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
        
    # 创建音频输出目录
    audio_dir = os.path.join('HF-day-paper-deepseek', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    
    # 读取论文数据
    json_file = os.path.join('HF-day-paper-deepseek', f"{date_str}_HF_deepseek_clean.json")
    if not os.path.exists(json_file):
        logger.error(f"未找到{date_str}的论文数据文件")
        return False
        
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
            
        # 生成语音稿
        script = f"欢迎收听Hugging Face {date_str}论文日报。今天为您带来{len(papers)}篇论文解读。\n\n"
        
        for i, paper in enumerate(papers, 1):
            translation = paper.get('translation', '')
            if '标题：' in translation and '摘要：' in translation:
                title = translation.split('标题：')[1].split('\n')[0]
                summary = translation.split('摘要：')[1].strip()
                script += f"第{i}篇论文：{title}\n{summary}\n\n"
        
        script += "感谢收听，我们明天再会。"
        
        # 生成语音文件
        output_path = os.path.join(audio_dir, f"{date_str}_daily_papers.mp3")
        success = await generate_audio(script, output_path)
        
        if success:
            logger.info(f"语音文件已生成：{output_path}")
            return True
        else:
            logger.error("生成语音文件失败")
            return False
            
    except Exception as e:
        logger.error(f"生成语音播报时出错：{str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(generate_daily_paper_audio()) 
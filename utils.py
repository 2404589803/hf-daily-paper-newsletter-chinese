import logging
import os
from datetime import datetime
import hashlib
import hmac
import time
import base64
from functools import wraps

# 默认配置
DEFAULT_MODEL = "deepseek-chat"
SUPPORTED_MODELS = {
    "deepseek-chat": "DeepSeek Chat",
}

def setup_logger():
    """设置日志记录器"""
    # 创建logs目录
    os.makedirs('logs', exist_ok=True)
    
    # 获取当前日期作为日志文件名
    log_file = os.path.join('logs', f"{time.strftime('%Y-%m-%d')}.log")
    
    # 配置日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def is_original_repo():
    """检查是否为原始仓库"""
    try:
        repo = os.getenv('GITHUB_REPOSITORY', '')
        return repo == '2404589803/hf-daily-paper-newsletter-chinese'
    except:
        return False

def validate_api_key(api_key):
    """验证API Key是否有效"""
    if not api_key or len(api_key) < 32:  # 简单的长度检查
        return False
    return True

def get_model_name():
    """获取要使用的模型名称"""
    return DEFAULT_MODEL  # 直接返回默认模型

def require_auth(func):
    """验证装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("未设置 DEEPSEEK_API_KEY 环境变量。如果这是一个fork的仓库，请在仓库的Settings->Secrets->Actions中设置您自己的DEEPSEEK_API_KEY。")
        
        # 验证API Key
        if not validate_api_key(api_key):
            raise ValueError("无效的 API Key 格式")
        
        # 如果是原始仓库，直接允许访问
        if is_original_repo():
            return func(*args, **kwargs)
        
        # 如果是fork的仓库，确保使用的是自己的API Key
        if api_key.startswith('sk-'):  # 假设这是一个新的API Key
            return func(*args, **kwargs)
        else:
            raise ValueError("Fork仓库必须使用自己的API Key。请在仓库的Settings->Secrets->Actions中设置您自己的DEEPSEEK_API_KEY。")
        
    return wrapper

def get_logger():
    """获取日志记录器"""
    return logging.getLogger('HF-daily-paper') 
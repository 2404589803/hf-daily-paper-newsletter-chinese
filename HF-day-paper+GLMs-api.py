import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

# 设置环境变量中的API地址和密钥，或者直接在代码中填写
BASE_URL = os.getenv("OPENAI_API_BASE", "http://8.130.209.127:8000/v1")
API_KEY = "51d5350a075931c7.fa2eab916c0705fd6b120434ddd98e96"  # 请替换为您的API密钥

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# 获取当天日期的前一天
yesterday = datetime.now() - timedelta(1)
yesterday_str = yesterday.strftime('%Y-%m-%d')

# 构建JSON文件的文件名
json_filename = f'{yesterday_str}.json'

# 尝试打开并读取JSON文件
try:
    with open(json_filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        file_content = json.dumps(data, ensure_ascii=False)  # 转换为JSON字符串
except FileNotFoundError:
    print(f"文件 {json_filename} 不存在")
    file_content = None
except json.JSONDecodeError:
    print(f"文件 {json_filename} 不是有效的JSON文件")
    file_content = None
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    file_content = None

# 如果文件内容成功读取，则调用OpenAI API进行处理
if file_content:
    try:
        # 调用对话补全接口
        result = client.chat.completions.create(
            model="65d6ba38fca9900836172419",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": file_content
                        },
                        {
                            "type": "text",
                            "text": "文档说了什么？"
                        }
                    ]
                }
            ],
            stream=False
        )

        # 输出调用结果
        print(result.choices[0].message.content)
    except Exception as e:
        print(f"调用OpenAI API时发生错误: {e}")
else:
    print("无法读取文件内容，未调用OpenAI API")

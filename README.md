# HF🤗每日简报机器人

该机器人能自动从 [🤗 Daily Papers](https://huggingface.co/papers) 收集paper信息，然后结合智能体进行解读。

# 🤗每日简报机器人如何工作？

1、获取 [🤗 Daily Papers](https://huggingface.co/papers) 中的所有paper信息

2、将收集到的paper信息使用 DeepSeek 模型进行解读，生成paper的中文解读信息

# 已自动化完成的功能

- [X] 自动从 [🤗 Daily Papers](https://huggingface.co/papers) 获取paper信息
- [X] 自动使用 DeepSeek API 进行论文解读，生成中文解读信息
- [X] 自动保存解读结果到JSON文件

# 使用方法

1. 克隆本仓库
2. 配置 DeepSeek API Key：
   - 访问您的 GitHub 仓库
   - 点击 "Settings" > "Security" > "Secrets and variables" > "Actions"
   - 点击 "New repository secret"
   - Name: `DEEPSEEK_API_KEY`
   - Value: 您的 DeepSeek API Key
   - 点击 "Add secret" 保存
3. 启用 GitHub Actions：
   - 访问仓库的 "Actions" 选项卡
   - 点击 "I understand my workflows, go ahead and enable them"
4. 运行方式：
   - 自动运行：每天北京时间 9:00 和 9:30 自动运行
   - 手动运行：在 Actions 页面选择工作流，点击 "Run workflow"

# 文件说明

- `Paper_metadata_download.py`: 下载论文元数据
- `HF-day-paper-deepseek.py`: 主程序
- `HF-day-paper-deepseek-clean.py`: 清理版本

# 未来预加入的功能

- 语音播报功能

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=2404589803/hf-daily-paper-newsletter-chinese&type=Date)](https://star-history.com/#2404589803/hf-daily-paper-newsletter-chinese&Date)
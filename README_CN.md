# HF🤗每日简报机器人
> [English Documentation](README.md)

该机器人能自动从 [🤗 Daily Papers](https://huggingface.co/papers) 收集paper信息，然后结合智能体进行解读。

## 🚀 主要功能

- ✅ 自动从 [🤗 Daily Papers](https://huggingface.co/papers) 获取paper信息
- ✅ 使用 DeepSeek API 进行智能论文解读
- ✅ 生成论文的中文解读信息
- ✅ 自动将解读结果保存为JSON文件

## 🛠️ 安装设置

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

## 🔄 运行方式

- **自动运行**：每天北京时间 9:00 和 9:30 自动运行
- **手动运行**：在 Actions 页面选择工作流，点击 "Run workflow"

## 📁 项目结构

- `Paper_metadata_download.py`: 下载论文元数据
- `HF-day-paper-deepseek.py`: 主程序
- `HF-day-paper-deepseek-clean.py`: 清理版本的主程序

## 🔜 即将推出的功能

- 语音播报功能

## ⭐ Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=2404589803/hf-daily-paper-newsletter-chinese&type=Date)](https://star-history.com/#2404589803/hf-daily-paper-newsletter-chinese&Date) 
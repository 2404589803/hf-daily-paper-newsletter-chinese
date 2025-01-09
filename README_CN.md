# HF🤗每日简报机器人
> [English Documentation](README.md)

该机器人能自动从 [🤗 Daily Papers](https://huggingface.co/papers) 收集paper信息，然后使用 DeepSeek 进行解读。

## 🚀 主要功能

- ✅ 自动从 [🤗 Daily Papers](https://huggingface.co/papers) 获取paper信息
- ✅ 使用 DeepSeek API 进行智能论文解读
- ✅ 生成论文的中文解读信息
- ✅ 自动生成每日论文海报
- ✅ 生成关键词云图和趋势分析
- ✅ 支持语音播报功能
- ✅ 自动生成日报（支持 Markdown 和 HTML 格式）
- ✅ 错误通知和自动重试机制

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
- `HF-day-paper-deepseek.py`: 主程序，处理论文解读
- `newsletter.py`: 生成日报
- `stats.py`: 统计分析和可视化
- `tts.py`: 语音合成
- `utils.py`: 工具函数

## 📊 数据分析

- **关键词云图**：直观展示热门研究主题
- **趋势分析**：显示每日论文数量变化
- **热门领域**：自动识别热门研究领域
- **统计报告**：生成详细的统计数据

## 📝 日报格式

- **Markdown 格式**：适合在 GitHub 上阅读
- **HTML 格式**：支持更丰富的展示效果
- **包含内容**：
  - 每日论文统计
  - 热门研究领域
  - 论文详细解读
  - 关键词云图
  - 趋势分析图
  - 语音播报链接

## 🎯 特色功能

- **智能翻译**：使用 DeepSeek API 进行专业的学术翻译
- **自动重试**：遇到错误时自动重试，提高可靠性
- **错误通知**：通过 GitHub Issues 自动通知运行错误
- **多语言支持**：提供中英文文档
- **数据可视化**：自动生成图表和统计信息

## ⭐ Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=2404589803/hf-daily-paper-newsletter-chinese&type=Date)](https://star-history.com/#2404589803/hf-daily-paper-newsletter-chinese&Date)

## 📄 许可证

本项目采用 MIT 许可证 
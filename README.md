# HF🤗 Daily Paper Newsletter Bot
> [中文文档](README_CN.md)

This bot automatically collects paper information from [🤗 Daily Papers](https://huggingface.co/papers) and uses DeepSeek for interpretation.

## 🚀 Key Features

- ✅ Automatic paper collection from [🤗 Daily Papers](https://huggingface.co/papers)
- ✅ Intelligent paper interpretation using DeepSeek API
- ✅ Chinese translation and analysis
- ✅ Automatic daily paper poster generation
- ✅ Keyword cloud and trend analysis
- ✅ Text-to-speech support
- ✅ Newsletter generation (Markdown & HTML)
- ✅ Error notification and auto-retry mechanism

## 🛠️ Setup

1. Clone this repository

2. Configure DeepSeek API Key:
   - Go to your GitHub repository
   - Click "Settings" > "Security" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name: `DEEPSEEK_API_KEY`
   - Value: Your DeepSeek API Key
   - Click "Add secret"

3. Enable GitHub Actions:
   - Go to the "Actions" tab
   - Click "I understand my workflows, go ahead and enable them"

## 🔄 Running

- **Automatic**: Runs daily at 9:00 and 9:30 Beijing Time
- **Manual**: Select workflow in Actions tab and click "Run workflow"

## 📁 Project Structure

- `Paper_metadata_download.py`: Download paper metadata
- `HF-day-paper-deepseek.py`: Main program for paper processing
- `newsletter.py`: Newsletter generation
- `stats.py`: Statistical analysis and visualization
- `tts.py`: Text-to-speech synthesis
- `utils.py`: Utility functions

### 📂 Directory Structure

- `HF-day-paper-deepseek/`: Processed paper data and daily summaries
- `Paper_metadata_download/`: Downloaded paper metadata
- `newsletters/`: Generated newsletter files (Markdown & HTML)
- `images/`: Newsletter images (keyword clouds, trend graphs, etc.)
- `audio/`: Audio broadcast files
- `stats/`: Statistical analysis data (JSON format)

## 📊 Data Analysis

- **Keyword Cloud**: Visual representation of hot research topics
- **Trend Analysis**: Daily paper count visualization
- **Hot Topics**: Automatic identification of trending research areas
- **Statistics Report**: Detailed statistical data generation

## 📝 Newsletter Format

- **Markdown Format**: Optimized for GitHub reading
- **HTML Format**: Rich presentation support
- **Contents Include**:
  - Daily paper statistics
  - Hot research areas
  - Detailed paper interpretations
  - Keyword cloud visualization
  - Trend analysis graph
  - Audio broadcast link

## 🎯 Special Features

- **Intelligent Translation**: Professional academic translation using DeepSeek API
- **Auto-retry**: Automatic retry on errors for improved reliability
- **Error Notification**: Automatic GitHub Issues creation for errors
- **Multilingual Support**: Chinese and English documentation
- **Data Visualization**: Automatic chart and statistics generation

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=2404589803/hf-daily-paper-newsletter-chinese&type=Date)](https://star-history.com/#2404589803/hf-daily-paper-newsletter-chinese&Date)

## 📄 License

This project is licensed under the MIT License
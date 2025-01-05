# HF Daily Papers Newsletter Bot 🤗
> [中文文档](README_CN.md)

An automated bot that collects and analyzes papers from [🤗 Daily Papers](https://huggingface.co/papers) using AI agents.

## 🚀 Features

- ✅ Automatic paper collection from [🤗 Daily Papers](https://huggingface.co/papers)
- ✅ AI-powered paper analysis using DeepSeek API
- ✅ Chinese translation and interpretation of paper content
- ✅ Automated JSON file storage for analysis results

## 🛠️ Setup

1. Clone this repository

2. Configure DeepSeek API Key:
   - Go to your GitHub repository
   - Navigate to "Settings" > "Security" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name: `DEEPSEEK_API_KEY`
   - Value: Your DeepSeek API Key
   - Click "Add secret" to save

3. Enable GitHub Actions:
   - Visit the "Actions" tab in your repository
   - Click "I understand my workflows, go ahead and enable them"

## 🔄 Running the Bot

- **Automated Running**: Runs daily at 9:00 and 9:30 (Beijing Time)
- **Manual Running**: Go to Actions page, select workflow, and click "Run workflow"

## 📁 Project Structure

- `Paper_metadata_download.py`: Downloads paper metadata
- `HF-day-paper-deepseek.py`: Main program
- `HF-day-paper-deepseek-clean.py`: Cleaned version of the main program

## 🔜 Upcoming Features

- Voice broadcasting functionality

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=2404589803/hf-daily-paper-newsletter-chinese&type=Date)](https://star-history.com/#2404589803/hf-daily-paper-newsletter-chinese&Date)
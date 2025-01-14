# Auto Crypto Agent

An automated cryptocurrency analysis system that fetches Bitcoin prices and relevant financial news, generates AI-powered analysis, and sends periodic email updates with price trend graphs.

## Customization

While this system is configured for Bitcoin price analysis, it can be easily adapted for other use cases:

- **Different Assets**: Modify `btc_agent.py` to track stocks, commodities, or other cryptocurrencies
- **Alternative News Sources**: Update `info_agent.py` to fetch news about any topic of interest
- **Custom Analysis**: Adjust the GPT-4 prompt in `email_agent.py` to focus on different aspects or topics
- **Varied Schedules**: Change the interval in `scheduler.py` to run at your preferred frequency

Example topics you could adapt this for:
- Stock market analysis
- Weather forecasting
- Sports statistics
- Social media trends
- News summarization

## Features

- 🤖 Automated Bitcoin price tracking
- 📰 Real-time financial news aggregation
- 🧠 AI-powered market analysis using GPT-4
- 📊 Price trend visualization
- 📧 Automated email reporting
- ⏰ Scheduled execution every 10 minutes

## System Architecture

The system consists of three main agents:
1. **BTC Agent**: Fetches latest Bitcoin prices
2. **Info Agent**: Gathers relevant financial news
3. **Email Agent**: Generates and sends analysis reports with price graphs

## Prerequisites

- Python 3.7+
- Virtual environment (recommended)
- Gmail account with App Password enabled
- OpenAI API key
- Brave API key
- Supabase account and credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/bitcoin-news-agent.git
cd bitcoin-news-agent
```

2. Create and activate virtual environment:
```
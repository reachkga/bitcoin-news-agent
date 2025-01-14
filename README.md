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
git clone https://github.com/reachkga/bitcoin-news-agent.git
cd bitcoin-news-agent
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Then edit `.env` with your actual credentials.

## Gmail App Password Setup

1. Go to your Google Account settings
2. Enable 2-Step Verification if not already enabled
3. Go to Security → App passwords
4. Select 'Mail' and 'Other (Custom name)'
5. Name it "Finance Agent"
6. Copy the generated 16-character password to your .env file

## Usage

1. Make the start and stop scripts executable:
```bash
chmod +x start_agents.sh stop_agents.sh
```

2. Start the agents:
```bash
./start_agents.sh
```

3. Monitor the logs:
```bash
tail -f logs/crypto_agents.log
tail -f logs/scheduler.log
```

4. Stop the agents:
```bash
./stop_agents.sh
```

## Logs

The system maintains two log files in the `logs` directory:
- `crypto_agents.log`: Contains execution logs of all agents
- `scheduler.log`: Contains scheduler-specific logs

## Configuration

- Default schedule: Every 10 minutes
- To modify the schedule, edit `scheduler.py`
- Email settings can be configured in `email_agent.py`
- Data fetching parameters can be adjusted in respective agent files

## Project Structure

```
bitcoin-news-agent/
├── btc_agent.py          # Bitcoin price fetching
├── info_agent.py         # News aggregation
├── email_agent.py        # Report generation and sending
├── scheduler.py          # Scheduling system
├── start_agents.sh       # Startup script
├── stop_agents.sh        # Shutdown script
├── requirements.txt      # Dependencies
├── .env.example         # Example environment variables
└── logs/                # Log files
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI GPT-4 for analysis
- Brave API for financial data
- Supabase for data storage
- Python Schedule library for task scheduling

## Support

For support, please open an issue in the GitHub repository.
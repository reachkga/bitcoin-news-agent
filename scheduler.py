import schedule
import time
import subprocess
import logging
import os
import sys
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')
    print(f"Created logs directory at {os.path.abspath('logs')}")

# Set up logging to both file and console
try:
    # Touch the log file to create it if it doesn't exist
    log_file = 'logs/crypto_agents.log'
    open(log_file, 'a').close()
    print(f"Touched log file at {os.path.abspath(log_file)}")
    
    # Set up logging handler for file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    
    # Set up logging handler for console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logging.info("Logging system initialized")
    print("Logging system initialized - Check both console and log files")
    
except Exception as e:
    print(f"Error setting up logging: {e}")
    raise

def run_agents():
    try:
        # Log start time
        logging.info("Starting agent sequence...")
        
        # Run btc_agent.py
        logging.info("Running BTC agent...")
        result = subprocess.run(['python', 'btc_agent.py'], check=True)
        if result.returncode == 0:
            logging.info("BTC agent completed successfully")
        
        # Run info_agent.py
        logging.info("Running Info agent...")
        result = subprocess.run(['python', 'info_agent.py'], check=True)
        if result.returncode == 0:
            logging.info("Info agent completed successfully")
        
        # Run email_agent.py
        logging.info("Running Email agent...")
        result = subprocess.run(['python', 'email_agent.py'], check=True)
        if result.returncode == 0:
            logging.info("Email agent completed successfully")
        
        logging.info("All agents completed successfully\n")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running agents: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")

def main():
    logging.info("Scheduler started")
    print("Scheduler started - Check logs/crypto_agents.log for details")
    
    # Schedule the job every 10 minutes
    schedule.every(10).minutes.do(run_agents)
    
    # Run once immediately on startup
    run_agents()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
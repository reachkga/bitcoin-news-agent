#!/bin/bash

# Create logs directory
mkdir -p logs
echo "Created logs directory"

# Activate virtual environment (if using one)
source venv/bin/activate
echo "Activated virtual environment"

# Kill any existing scheduler processes
pkill -f "python scheduler.py"
echo "Cleaned up any existing scheduler processes"

# Start the scheduler in the background but keep output visible
nohup python scheduler.py > logs/scheduler.log 2>&1 &
SCHEDULER_PID=$!
echo "Started scheduler with PID: $SCHEDULER_PID"

# Verify the process is running
if ps -p $SCHEDULER_PID > /dev/null; then
    echo "Scheduler is running successfully"
    # Save the process ID
    echo $SCHEDULER_PID > logs/process.pid
    echo "Saved PID to logs/process.pid"
    
    # Wait a moment for logs to be created
    sleep 2
    
    # Show initial logs if they exist
    if [ -f logs/scheduler.log ]; then
        echo -e "\nInitial scheduler logs:"
        tail -n 5 logs/scheduler.log
    fi
    
    if [ -f logs/crypto_agents.log ]; then
        echo -e "\nInitial crypto agents logs:"
        tail -n 5 logs/crypto_agents.log
    fi
else
    echo "Error: Scheduler failed to start"
    exit 1
fi

echo -e "\nAgents started successfully. Monitor logs with:"
echo "tail -f logs/scheduler.log"
echo "tail -f logs/crypto_agents.log"
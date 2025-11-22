#!/bin/bash

# Get the absolute path to the run_daily.sh script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
RUN_SCRIPT="$SCRIPT_DIR/run_daily.sh"

# Make the script executable
chmod +x "$RUN_SCRIPT"

# Define the cron job (run at 9:00 AM every day)
CRON_JOB="0 9 * * * $RUN_SCRIPT"

# Check if the job already exists
(crontab -l 2>/dev/null | grep -F "$RUN_SCRIPT") && echo "Cron job already exists" && exit 0

# Add the cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Cron job added successfully. It will run daily at 9:00 AM."
echo "To view your cron jobs, run: crontab -l"

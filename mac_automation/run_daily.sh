#!/bin/bash

# Navigate to the project directory
# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$SCRIPT_DIR"

cd "$PROJECT_DIR"

# Check if virtual environment exists, if so activate it
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if needed (simple check)
pip install -r requirements.txt > /dev/null 2>&1

# Run the python script
python local_main.py >> "$SCRIPT_DIR/automation.log" 2>&1

echo "Ran expense automation at $(date)" >> "$SCRIPT_DIR/automation.log"

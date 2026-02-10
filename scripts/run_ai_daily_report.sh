#!/bin/bash
# Script to run the daily AI and GitHub report

# Set the path to your anaconda python
PYTHON_PATH="/Users/fanshengxia/opt/anaconda3/bin/python"

# Set the path to your script
SCRIPT_PATH="/Users/fanshengxia/clawd/scripts/ai_github_daily_report.py"

# Change to the working directory
cd /Users/fanshengxia/clawd

# Run the Python script
$PYTHON_PATH $SCRIPT_PATH

# Optionally, save output to a log file
# $PYTHON_PATH $SCRIPT_PATH >> /Users/fanshengxia/clawd/logs/ai_daily_report_$(date +%Y%m%d).log 2>&1
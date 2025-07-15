#!/bin/bash

mkdir -p "/home/gtxr/gtxr-picamera/logs"
exec >> "/home/gtxr/gtxr-picamera/logs/main_log.txt" 2>&1
set -x

# Absolute path to your project directory
PROJECT_DIR="/home/gtxr/gtxr-picamera"
date=$(date +%Y-%m-%d_%H-%M-%S)
TOP_LOG="/home/gtxr/gtxr-picamera/logs/main_log_${date}.txt"

mkdir -p "/home/gtxr/gtxr-picamera/logs"
exec >> "/home/gtxr/gtxr-picamera/logs/$TOP_LOG" 2>&1

# Navigate to the project directory
cd "$PROJECT_DIR"

# Activate the virtual environment
source "picamvenv/bin/activate"

# Check that the background process is running
if ! pgrep -f "automatic_picam.py" > /dev/null; then
    echo "$(date): Starting automatic picam manager" >> "$TOP_LOG"
    sudo /home/gtxr/gtxr-picamera/picamvenv/bin/python -u automatic_picam.py
else
    echo "$(date): $SCRIPT already running" >> "$TOP_LOG"
fi
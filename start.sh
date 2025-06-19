#!/bin/bash

# AnswerCustomer start script (macOS/Linux)

echo "============================================================"
echo "[32m AnswerCustomer Start Script (macOS/Linux)"
echo "============================================================"
echo

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[31m Python3 is not installed."
    echo "Please install Python 3.7 or higher."
    echo "macOS: brew install python3"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "[32m Python3 is installed."
echo

# Check if script is executable
if [ ! -x "init_and_run.py" ]; then
    echo "[33m Setting script executable permission..."
    chmod +x init_and_run.py
fi

# Run initialization script
echo "Starting AnswerCustomer..."
python3 init_and_run.py

if [ $? -ne 0 ]; then
    echo
    echo "[31m Start failed, please check error messages."
    exit 1
fi 
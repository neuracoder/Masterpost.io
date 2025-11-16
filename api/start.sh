#!/bin/bash

echo "========================================"
echo " Starting Masterpost API (Qwen Only)"
echo "========================================"
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your keys."
    exit 1
fi

# Start server
echo "Starting server on http://localhost:8000"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000

#!/bin/sh
# Startup script for Moroccan Education API
# Changes to script directory and starts uvicorn

# Change to the directory where this script is located
cd "$(dirname "$0")"

PORT="${PORT:-8000}"
echo "Starting API on port $PORT from $(pwd)"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"

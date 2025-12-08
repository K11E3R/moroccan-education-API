#!/bin/sh
# Startup script for Moroccan Education API
# Uses PORT env var or defaults to 8000

PORT="${PORT:-8000}"
echo "Starting API on port $PORT"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"


#!/bin/sh
# Startup script for Moroccan Education API v1.0

cd "$(dirname "$0")/.."

export PYTHONPATH="${PYTHONPATH:-$(pwd)}"
PORT="${PORT:-8000}"

echo "================================================"
echo "  Moroccan Education API v1.0"
echo "  Port: $PORT | PYTHONPATH: $PYTHONPATH"
echo "================================================"

exec python3 -m uvicorn api.main:app --host 0.0.0.0 --port "$PORT"

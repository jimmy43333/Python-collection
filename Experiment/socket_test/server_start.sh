#!/usr/bin/env bash
set -euo pipefail
# 環境變數可調整:
#   PORT 預設 5000
#   INTERVAL 記憶體紀錄間隔秒 (預設 1)
HOST=0.0.0.0
PORT=5555
MEM_INTERVAL=${INTERVAL:-1}

echo Start server...
python3 socket/threadPool_server.py --ip $HOST --port "$PORT"
# python3 socket/simple_server.py --ip $HOST --port "$PORT"
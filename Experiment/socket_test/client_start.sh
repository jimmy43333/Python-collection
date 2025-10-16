#!/usr/bin/env bash
set -euo pipefail
# 環境變數可調整:
#   PORT / HOST / CLIENTS / COUNT / MODE / SEND_INTERVAL / MEM_INTERVAL
HOST=172.17.0.1
PORT=5555
CLIENTS=1000
COUNT=100
# MODE=persistent
MODE=reconnect
MSGLen=100
INT=0.1

sleep 5
echo Start clients...
python3 socket/multi_client.py --ip $HOST --port $PORT --clients $CLIENTS --count $COUNT --mode $MODE -ml $MSGLen --interval $INT

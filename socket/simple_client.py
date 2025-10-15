#!/usr/bin/env python3
"""簡易 TCP Socket Client
輸入文字送到伺服器, 回應顯示. 輸入 quit 結束.
"""
import socket
import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib import get_logger

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
BUFFER_SIZE = 4096
logger = get_logger('socket_client', logfile=os.path.join(LOG_DIR, 'socket_client.log'))


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Simple TCP socket client")
    p.add_argument('--ip', default="127.0.0.1", help="Server host (default 127.0.0.1)")
    p.add_argument('-p', '--port', type=int, default=5000, help="Server port (default 5000)")
    p.add_argument('-m', '--message', help="Send single message then exit", nargs="?")
    return p.parse_args(argv)


def interactive(sock: socket.socket):
    try:
        while True:
            line = input("輸入文字 (quit 結束): ").strip()
            if not line:
                continue
            sock.sendall((line + "\n").encode())
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("[Server closed]")
                break
            logger.info(f"SEND {line}")
            logger.info("REPLY %s", data.decode(errors="ignore").rstrip())
            print("[REPLY]", data.decode(errors="ignore").rstrip())
            if line.lower() == "quit":
                break
    except (EOFError, KeyboardInterrupt):
        print("\n[Abort]")


def single_message(sock: socket.socket, msg: str):
    sock.sendall((msg + "\n").encode())
    data = sock.recv(BUFFER_SIZE)
    logger.info(f"SEND {msg}")
    logger.info("REPLY %s", data.decode(errors="ignore").rstrip())
    print(data.decode(errors="ignore").rstrip())


def main():
    args = parse_args()
    try:
        with socket.create_connection((args.ip, args.port), timeout=10) as sock:
            if args.message is not None:
                single_message(sock, args.message)
            else:
                interactive(sock)
    except Exception as e:
        logger.exception(f"ERROR {e}")
        print(f"[ERROR] {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

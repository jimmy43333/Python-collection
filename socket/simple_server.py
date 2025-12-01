#!/usr/bin/env python3
"""簡易 TCP Socket Server
啟動後接受多個連線, 每行資料回傳成大寫.
Ctrl+C 可中止.
"""
import socket
import threading
import argparse
import sys
import os  # 新增
# 允許直接在 socket 目錄執行 (python socket_server.py) 時可找到上層 lib 模組
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib import get_logger

# 專案根目錄 logs 位置
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
BUFFER_SIZE = 4096
logger = get_logger('socket_server', logfile=os.path.join(LOG_DIR, 'socket_server.log'))


def handle_client(conn: socket.socket, addr):
    logger.info(f"CONNECTED {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                text = data.decode(errors="ignore").strip()
                logger.info(f"RECV {addr} {text}")
                if text.lower() == "quit":
                    conn.sendall(b"Bye\n")
                    break
                response = (text.upper() + "\n").encode()
                conn.sendall(response)
    except Exception as e:
        logger.exception(f"ERROR {addr} {e}")
    finally:
        logger.info(f"CLOSED {addr}")


def run_socket_server(host: str, port: int):
    logger.info(f"START Server listening on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            logger.info("SHUTDOWN Server stopping...")
        except Exception as e:
            logger.exception(f"FATAL {e}")
    logger.info("EXIT")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Simple TCP socket server")
    p.add_argument("--ip", default="0.0.0.0", help="Bind host (default 0.0.0.0)")
    p.add_argument("-p", "--port", type=int, default=5000, help="Bind port (default 5000)")
    return p.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    run_socket_server(args.ip, args.port)

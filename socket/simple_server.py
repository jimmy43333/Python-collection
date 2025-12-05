#!/usr/bin/env python3
"""TCP Socket Server
啟動後接受多個連線.
"""
import sys
import os
import socket
import concurrent.futures
import threading
import argparse

# 允許直接在 socket 目錄執行 (python socket_server.py) 時可找到上層 lib 模組
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib import get_logger

# 專案根目錄 logs 位置
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logger = get_logger('socket_server', logfile=os.path.join(LOG_DIR, 'socket_server.log'))

SERVER_ACCEPT = 168
MAX_WORKERS = 300
SERVER_RUNNING = True
CLIENT_BUFFER_SIZE = 512
CLIENT_TIMEOUT = 10

def handle_client(client_socket, idle_break=False):
    client_socket.settimeout(CLIENT_TIMEOUT)
    client_name = client_socket.getpeername()
    temp = ""
    count = 0
    FRAGMENT_MAX = CLIENT_BUFFER_SIZE * 2
    while SERVER_RUNNING:
        try:
            request = client_socket.recv(CLIENT_BUFFER_SIZE).decode()
            count = 0
            if not request:
                break
            temp += request
            line = temp.split("\n")
            # 資料結尾不是換行符號，表示資料還沒接收完整，將最後一筆存入 temp
            if line[-1] == "":
                temp = ""
                line.pop()
            else:
                temp = line.pop()
                # 預防 fragment 資料持續增大
                if len(temp) > FRAGMENT_MAX:
                    msg = f"Fragment data exceed [{FRAGMENT_MAX}]: " \
                          f"Break {client_name[0]} !!"
                    logger.warning(msg)
                    break
            for ele in line:
                output = ele.strip()
                if not output:
                    continue
                # Handle Your Data Here
                logger.info(output)
            client_socket.send("ACK!".encode())
        except socket.timeout:
            if not idle_break:
                continue
            count += 1
            # 連線閒置超過 CLIENT_TIMEOUT * 10 秒會自動斷線
            if count >= 10:
                msg = f"[x] Client Idle (> {CLIENT_TIMEOUT * count} secs)," \
                      f"Disconnect: {client_name} !"
                logger.info(msg)
                break
        except socket.error as err:
            msg = f"Socket client {client_name} error and Break: {err}"
            logger.warning(msg)
            break
        except Exception as e:
            logger.error(f"handle_client: {str(e)}")
    if client_socket:
        client_socket.close()


def run_socket_server(host: str, port: int):
    logger.info(f"START Server listening on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(SERVER_ACCEPT)
        server_socket.settimeout(60)
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as client_executor:
            while SERVER_RUNNING:
                try:
                    client, addr = server_socket.accept()
                    t = threading.active_count()
                    pt = len(client_executor._threads)
                    msg = f"[*] Accepted from: {addr[0]}:{addr[1]} (T:{t}, PT:{pt})"
                    logger.info(msg)
                    client_executor.submit(handle_client, client, True)
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break
        server_socket.close()


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Simple TCP socket server")
    p.add_argument("--ip", default="0.0.0.0", help="Bind host (default 0.0.0.0)")
    p.add_argument("-p", "--port", type=int, default=5000, help="Bind port (default 5000)")
    return p.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    run_socket_server(args.ip, args.port)

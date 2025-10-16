#!/usr/bin/env python3
"""ThreadPoolExecutor TCP Socket Server
啟動後接受多個連線
Ctrl+C 可中止.
"""
import socket
import threading
import concurrent.futures
import argparse
import sys
import os
import json
from dataclasses import dataclass, field
from typing import Callable, Optional, Iterable

# 允許直接在 socket 目錄執行 (python socket_server.py) 時可找到上層 lib 模組
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib import get_logger

# 專案根目錄 logs 位置
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logger = get_logger('socket_server', logfile=os.path.join(LOG_DIR, 'socket_server.log'))


@dataclass
class SocketServerConfig:
    """Configuration & callbacks for fragment socket server."""
    # network / protocol
    socket_accept: int = 168
    socket_len: int = 4096
    ## seconds per recv()
    socket_idle_timeout: int = 10
    ## consecutive timeouts before disconnect when idle_break enabled
    socket_idle_timeout_retry: int = 3
    max_workers: int = 300
    # new: accept() timeout (seconds) so loop can periodically check running flag
    accept_timeout: float = 10.0
    # runtime flags
    socket_running: bool = True
    # parsing & handling functions
    check_data_function: Callable[[str], Optional[dict]] = lambda line: None
    handle_data_function: Callable[[dict], None] = lambda data: None
    # IPs that should trigger idle break mode
    socket_idle_break_list: Iterable[str] = field(default_factory=list)
    # logging helpers
    log: Callable[[str], None] = lambda msg: logger.info(msg)


def handle_client(client_socket: socket.socket, config: SocketServerConfig, idle_break: bool = False):
    """Receive potentially fragmented newline-delimited JSON messages.

    Each message is expected to be a JSON object terminated by a newline. If a
    partial ("Fragment") token is received we buffer until completed. After each
    processed message we send back a simple ACK.
    """
    temp = ""
    count = 0
    peer = None
    try:
        peer = client_socket.getpeername()
    except Exception:
        pass
    client_socket.settimeout(config.socket_idle_timeout)
    while config.socket_running:
        try:
            raw = client_socket.recv(config.socket_len)
            if not raw:
                break
            request = raw.decode(errors="ignore")
            count = 0  # reset timeout counter on successful recv
            request = temp + request
            temp = ""
            # split by newline boundaries
            lines = request.split("\n")
            for line in lines:
                if not line:
                    continue
                result = config.check_data_function(line)
                if result is None:
                    temp = line
                    continue
                config.handle_data_function(result)
            client_socket.sendall(b"ACK!\n")
        except socket.timeout:
            if idle_break:
                count += 1
                if count >= config.socket_idle_timeout_retry:
                    duration = config.socket_idle_timeout * count
                    msg = f"[x] Client Idle (> {duration} secs), Disconnect: {peer} !"
                    config.log(msg)
                    break
            continue
        except socket.error:
            break
        except Exception as e:
            config.log(f"handle_client_fragment: {e}")
            break
    try:
        client_socket.close()
    finally:
        config.log(f"[-] Closed {peer}")


def run_socket_server(ip: str, port: int, config: SocketServerConfig, background: bool = False):
    """Run a socket server that uses handle_client_fragment. If background=True returns the thread.

    You can call this multiple times with different ip/port & configs to run several servers.
    """
    bind_ip = ip
    bind_port = int(port)

    def _serve():
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((bind_ip, bind_port))
            server_socket.listen(config.socket_accept)
            # set accept timeout so we can periodically re-check socket_running
            server_socket.settimeout(config.accept_timeout)
        except Exception as e:
            raise
        config.log(f"[*] Listening on {bind_ip}:{bind_port}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers) as client_executor:
            while config.socket_running:
                try:
                    client, addr = server_socket.accept()
                    t = threading.active_count()
                    pt = len(client_executor._threads)
                    t_type = '*'
                    flag = False
                    if config.socket_idle_break_list and addr[0] in config.socket_idle_break_list:
                        t_type = '#'
                        flag = True
                    msg = f"[{t_type}] Accepted from: {addr[0]}:{addr[1]} (T:{t}, PT:{pt})"
                    config.log(msg)
                    client_executor.submit(handle_client, client, config, flag)
                except socket.timeout:
                    # timeout just allows loop to check socket_running again
                    continue
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    config.log(f"accept loop error: {e}")
                    break
        try:
            server_socket.close()
        finally:
            config.log(f"[!] Server closed {bind_ip}:{bind_port}")

    if background:
        thread = threading.Thread(target=_serve, name=f"SocketServer-{bind_ip}:{bind_port}", daemon=True)
        thread.start()
        return thread
    else:
        _serve()
        return None

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Simple TCP socket server")
    p.add_argument("--ip", default="0.0.0.0", help="Bind host (default 0.0.0.0)")
    p.add_argument("-p", "--port", type=int, default=5000, help="Bind port (default 5000)")
    return p.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()

    def check_data(line: str) -> Optional[dict]:
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None  # 視為尚未收齊的片段

    def handle_data(data: dict):
        print("SID handler got:", data)

    cfg = SocketServerConfig(
        socket_accept=100,
        socket_len=256,
        socket_idle_timeout=10,
        socket_idle_timeout_retry=3,
        max_workers=300,
        check_data_function=check_data,
        handle_data_function=handle_data,
        socket_idle_break_list=["127.0.0.1"],
        accept_timeout=1.0,
    )

    # 前景執行 (阻塞)
    run_socket_server(args.ip, args.port, cfg)

    # 或背景執行多個
    # t1 = run_socket_server(args.ip, args.port, cfg, background=True)
    # t2 = run_socket_server("0.0.0.0", 6002, cfg, background=True)
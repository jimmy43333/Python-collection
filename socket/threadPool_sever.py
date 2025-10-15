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
import concurrent.futures
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Iterable, Any

# 允許直接在 socket 目錄執行 (python socket_server.py) 時可找到上層 lib 模組
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib import get_logger

# 專案根目錄 logs 位置
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
BUFFER_SIZE = 4096
logger = get_logger('socket_server', logfile=os.path.join(LOG_DIR, 'socket_server.log'))

@dataclass
class SocketServerConfig:
    """Configuration & callbacks for fragment socket server."""
    # network / protocol
    socket_len: int = BUFFER_SIZE
    socket_idle_timeout: int = 10               # seconds per recv()
    socket_idle_timeout_retry: int = 3          # consecutive timeouts before disconnect when idle_break enabled
    max_workers: int = 300
    # runtime flags
    socket_running: bool = True
    socket_len_alert: bool = False
    # optional publisher with a method pub_ats_alert(msg, level?)
    publisher: Optional[Any] = None
    # map SID -> handler callable(dict)
    handle_data_function: Dict[str, Callable[[dict], None]] = field(default_factory=dict)
    # IPs that should trigger idle break mode
    socket_idle_break_list: Iterable[str] = field(default_factory=list)
    # logging helpers
    log_debug_data: Callable[[str], None] = lambda msg: logger.debug(msg)
    log: Callable[[str], None] = lambda msg: logger.error(msg)


def handle_client_fragment(client_socket: socket.socket, config: SocketServerConfig, idle_break: bool = False):
    """Receive potentially fragmented newline-delimited JSON messages.

    Each message is expected to be a JSON object terminated by a newline. If a
    partial ("Fragment") token is received we buffer until completed. After each
    processed message we send back a simple ACK.
    """
    client_socket.settimeout(config.socket_idle_timeout)
    temp = ""
    count = 0
    peer = None
    try:
        peer = client_socket.getpeername()
        config.log_debug_data(f"[+] Connected {peer}")
    except Exception:
        pass

    while config.socket_running:
        try:
            raw = client_socket.recv(config.socket_len)
            if not raw:
                break
            request = raw.decode(errors="ignore")
            count = 0  # reset timeout counter on successful recv

            # alert once if request >= socket_len (possible truncation risk)
            if len(request) >= config.socket_len and not config.socket_len_alert:
                alert_msg = f"(Publish alert ONCE) socket package len {config.socket_len}: {request[:200]}..."
                if config.publisher and hasattr(config.publisher, "pub_ats_alert"):
                    try:
                        config.publisher.pub_ats_alert(alert_msg, "O")
                    except Exception:
                        logger.debug("publisher alert failed")
                config.socket_len_alert = True

            request = temp + request
            temp = ""
            # split by newline boundaries
            lines = request.split("\n")
            for line in lines:
                if not line:
                    continue
                if line == "Fragment":  # placeholder fragment marker
                    temp = line
                    continue
                parsed_dictionary = None
                # Try parse JSON; if fails treat as plain text
                try:
                    parsed_dictionary = json.loads(line)
                except Exception:
                    parsed_dictionary = {"SID": "TEXT", "DATA": line}
                # dispatch
                sid = parsed_dictionary.get("SID")
                if sid and sid in config.handle_data_function:
                    try:
                        config.handle_data_function[sid](parsed_dictionary)
                    except Exception as e:
                        config.log(f"handler {sid} error: {e}")
                else:
                    config.log_debug_data(f"[?] No handler for SID={sid}")

            client_socket.sendall(b"ACK!\n")
        except socket.timeout:
            if idle_break:
                count += 1
                if count >= config.socket_idle_timeout_retry:
                    duration = config.socket_idle_timeout * count
                    try:
                        who = client_socket.getpeername()
                    except Exception:
                        who = peer
                    msg = f"[x] Client Idle (> {duration} secs), Disconnect: {who} !"
                    config.log_debug_data(msg)
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
        config.log_debug_data(f"[-] Closed {peer}")


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
            server_socket.listen(168)
        except Exception as e:
            if config.publisher and hasattr(config.publisher, "pub_ats_alert"):
                try:
                    config.publisher.pub_ats_alert(str(e))
                except Exception:
                    pass
            raise
        config.log_debug_data(f"[*] Listening on {bind_ip}:{bind_port}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers) as client_executor:
            while config.socket_running:
                try:
                    client, addr = server_socket.accept()
                    t = threading.active_count()
                    pt = len(client_executor._threads)
                    # determine idle_break flag
                    if config.socket_idle_break_list and addr[0] in config.socket_idle_break_list:
                        msg = f"[*] Accepted from: {addr[0]}:{addr[1]}, Enable Break (T:{t}, PT:{pt})"
                        flag = True
                    else:
                        msg = f"[*] Accepted from: {addr[0]}:{addr[1]} (T:{t}, PT:{pt})"
                        flag = False
                    config.log_debug_data(msg)
                    client_executor.submit(handle_client_fragment, client, config, flag)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    config.log(f"accept loop error: {e}")
                    break
        try:
            server_socket.close()
        finally:
            config.log_debug_data(f"[!] Server closed {bind_ip}:{bind_port}")

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
    def demo_handler(data: dict):
        print("SID handler got:", data)

    cfg = SocketServerConfig(
        handle_data_function={"TEXT": demo_handler},
        socket_idle_break_list=["127.0.0.1"]  # 啟用 idle break 的 ip
    )

    # 前景執行 (阻塞)
    run_socket_server("0.0.0.0", 6000, cfg)

    # 或背景執行多個
    t1 = run_socket_server("0.0.0.0", 6001, cfg, background=True)
    t2 = run_socket_server("0.0.0.0", 6002, cfg, background=True)
#!/usr/bin/env python3
"""多連線多執行緒 TCP Socket Client
依參數建立多個連線, 以兩種模式傳送資料:

模式:
- persistent: 每個執行緒建立一個持久連線, 連線期間不斷傳送 (原本行為)
- reconnect: 每一筆封包都重新建立一次 socket 連線, 傳送/接收後立即關閉

功能:
1. --clients 指定同時建立幾個連線 (執行緒)
2. --count 指定每個連線要傳送的總封包數量; 若 --count=0 則持續傳送直到中斷
3. 每個 client 的訊息內容帶有 client 編號與序號便於分辨
4. --mode 選擇 persistent 或 reconnect
5. log 會記錄不同 client 的傳送與回應結果 (socket_multi_client.log)

使用範例:
    python multi_client.py --ip 127.0.0.1 --port 5000 --clients 5 --count 100 --message "ping" --interval 0.01
    python multi_client.py --clients 3 --count 0 --message test --mode persistent
    python multi_client.py --clients 2 --count 50 --message hi --mode reconnect --interval 0.005
"""
import socket
import threading
import argparse
import time
import sys
import os
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib import get_logger  # noqa: E402

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
BUFFER_SIZE = 4096
logger = get_logger('socket_multi_client', logfile=os.path.join(LOG_DIR, 'socket_multi_client.log'))


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Multi-thread TCP socket client")
    p.add_argument('--ip', default='127.0.0.1', help='Server host (default 127.0.0.1)')
    p.add_argument('-p', '--port', type=int, default=5000, help='Server port (default 5000)')
    p.add_argument('-c', '--clients', type=int, default=1, help='同時建立連線/執行緒數量 (default 1)')
    p.add_argument('--count', type=int, default=10, help='每個連線欲傳送的封包數量 (0 代表持續傳送)')
    p.add_argument('-m', '--message', default='hello', help='基本訊息字串前綴 (default hello)')
    p.add_argument('--interval', type=float, default=0.05, help='每次送出後睡眠秒數 (default 0.05)')
    p.add_argument('--timeout', type=float, default=5.0, help='連線/每次建立逾時秒數 (default 5)')
    p.add_argument('--mode', choices=['persistent', 'reconnect'], default='persistent', help='連線模式 persistent 或 reconnect (default persistent)')
    return p.parse_args(argv)


class ClientWorker(threading.Thread):
    def __init__(self, cid: int, host: str, port: int, base_msg: str, count: int, interval: float, timeout: float, mode: str, stop_event: threading.Event):
        super().__init__(daemon=True)
        self.cid = cid
        self.host = host
        self.port = port
        self.base_msg = base_msg
        self.count = count
        self.interval = interval
        self.timeout = timeout
        self.mode = mode  # persistent | reconnect
        self.stop_event = stop_event
        self.sent = 0
        self.received = 0
        self.errors: int = 0

    def run(self):
        if self.mode == 'persistent':
            self._run_persistent()
        else:
            self._run_reconnect()

    def _run_persistent(self):
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
                logger.info(f"[client {self.cid}] CONNECTED {self.host}:{self.port} mode=persistent count={self.count}")
                i = 0
                while not self.stop_event.is_set():
                    if self.count > 0 and i >= self.count:
                        break
                    msg = f"{self.base_msg}-client{self.cid}-seq{i}"
                    try:
                        sock.sendall((msg + "\n").encode())
                        self.sent += 1
                        data = sock.recv(BUFFER_SIZE)
                        if not data:
                            logger.info(f"[client {self.cid}] SERVER_CLOSED")
                            break
                        reply = data.decode(errors='ignore').strip()
                        self.received += 1
                    except Exception as e:
                        self.errors += 1
                        logger.error(f"[client {self.cid}] ERROR {e}")
                        break
                    i += 1
                    if self.interval > 0:
                        time.sleep(self.interval)
                    elif self.count == 0:
                        time.sleep(0)
        except Exception as e:
            self.errors += 1
            logger.error(f"[client {self.cid}] CONNECT_ERROR {e}")
        finally:
            logger.info(f"[client {self.cid}] CLOSED sent={self.sent} recv={self.received} errors={self.errors}")

    def _run_reconnect(self):
        logger.info(f"[client {self.cid}] START mode=reconnect count={self.count}")
        i = 0
        while not self.stop_event.is_set():
            if self.count > 0 and i >= self.count:
                break
            msg = f"{self.base_msg}-client{self.cid}-seq{i}"
            try:
                with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
                    logger.debug(f"[client {self.cid}] OPEN seq={i}")
                    sock.sendall((msg + "\n").encode())
                    self.sent += 1
                    data = sock.recv(BUFFER_SIZE)
                    if data:
                        reply = data.decode(errors='ignore').strip()
                        self.received += 1
                    # 連線自動關閉 (with)
            except Exception as e:
                self.errors += 1
                logger.error(f"[client {self.cid}] RECONNECT_ERROR seq={i} {e}")
            i += 1
            if self.interval > 0:
                time.sleep(self.interval)
            elif self.count == 0:
                time.sleep(0)
        logger.info(f"[client {self.cid}] FINISH mode=reconnect sent={self.sent} recv={self.received} errors={self.errors}")


def main(argv: Optional[list] = None) -> int:
    args = parse_args(argv)
    stop_event = threading.Event()

    workers = [
        ClientWorker(cid=i + 1, host=args.ip, port=args.port, base_msg=args.message,
                     count=args.count, interval=args.interval,
                     timeout=args.timeout, mode=args.mode, stop_event=stop_event)
        for i in range(args.clients)
    ]

    logger.info(f"START multi-client host={args.ip} port={args.port} clients={args.clients} count={args.count} interval={args.interval} mode={args.mode}")

    try:
        for w in workers:
            w.start()
        while any(w.is_alive() for w in workers):
            for w in workers:
                w.join(timeout=0.2)
    except KeyboardInterrupt:
        logger.info("INTERRUPT received, stopping all clients...")
        stop_event.set()
        for w in workers:
            w.join()
    except Exception as e:
        logger.error(f"FATAL {e}")
        stop_event.set()
        for w in workers:
            w.join()
        return 1

    total_sent = sum(w.sent for w in workers)
    total_recv = sum(w.received for w in workers)
    total_err = sum(w.errors for w in workers)
    logger.info(f"SUMMARY mode={args.mode} sent={total_sent} recv={total_recv} errors={total_err}")
    print(f"SUMMARY mode={args.mode} sent={total_sent} recv={total_recv} errors={total_err}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

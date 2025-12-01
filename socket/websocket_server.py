#!/usr/bin/env python3
"""
獨立通訊的 WebSocket Server
每個客戶端可以訂閱不同的數據流，獨立接收數據
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Set, Dict
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
import threading
import time
import uuid

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebSocketServer:
    def __init__(self, host="0.0.0.0", port=8765, ack_timeout=5.0, max_retries=3, logger=None):
        self.host = host
        self.port = port
        self.ack_timeout = ack_timeout
        self.max_retries = max_retries
        self.logger = logger

        self.loop = None
        self.server = None
        self.thread = None

        self.clients = set()
        self.message_queue = asyncio.Queue()  # thread-safe broadcast queue

        # ACK mechanism
        self.pending_messages = {}  # {message_id: {client: websocket, data: dict, retries: int, timestamp: float}}
        self.client_info = {}  # {websocket: {id: str, connected_at: float}}

    def log(self, msg):
        """Log message using provided logger or fallback to print"""
        if self.logger:
            self.logger.info(msg)
        else:
            print(msg)

    # ------------------------------------------------------
    # Public API
    # ------------------------------------------------------
    def start(self):
        """Start the WebSocket server in a background thread"""
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

        # Wait for loop ready
        while self.loop is None:
            time.sleep(0.01)

        self.log("[WS] Server thread started")

    def stop(self):
        """Stop the WebSocket server"""
        if self.loop and self.server:
            asyncio.run_coroutine_threadsafe(self._stop_server(), self.loop)

    def broadcast(self, item, require_ack=False):
        """Thread-safe method to send data to all clients"""
        if self.loop is None:
            self.log("[WS] Cannot broadcast: loop not ready")
            return

        # Add message ID if ACK is required
        if require_ack:
            item["message_id"] = str(uuid.uuid4())
            item["require_ack"] = True

        msg = json.dumps(item)

        # Put message to async queue safely from any thread
        asyncio.run_coroutine_threadsafe(self.message_queue.put(msg), self.loop)

    # ------------------------------------------------------
    # Internal
    # ------------------------------------------------------
    def _run_loop(self):
        """Runs an entire asyncio loop in its own thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self._start_server())
        self.loop.create_task(self._broadcast_worker())
        self.loop.run_forever()

    async def _start_server(self):
        self.server = await websockets.serve(
            self._handle_client, self.host, self.port
        )
        self.log(f"[WS] Server listening on ws://{self.host}:{self.port}")

    # ------------------------------------------------------
    # Client handling
    # ------------------------------------------------------
    async def _handle_client(self, websocket):
        """Handle a single client connection"""
        self.clients.add(websocket)

        # Store client info
        client_id = str(uuid.uuid4())
        self.client_info[websocket] = {
            "id": client_id,
            "connected_at": time.time()
        }

        self.log(f"[WS] Client {client_id} connected ({len(self.clients)} total)")

        try:
            async for message in websocket:
                await self._handle_client_message(websocket, message)

        except (ConnectionClosedOK, ConnectionClosedError):
            self.log(f"[WS] Client {client_id} disconnected")

        except Exception as e:
            self.log(f"[WS] Client {client_id} exception: {e}")

        finally:
            self.clients.discard(websocket)
            if websocket in self.client_info:
                del self.client_info[websocket]
            self.log(f"[WS] Client {client_id} removed ({len(self.clients)} total)")

    # ------------------------------------------------------
    # Broadcast handler (runs in server loop)
    # ------------------------------------------------------
    async def _broadcast_worker(self):
        """Worker that sends queued messages to all clients"""
        while True:
            msg = await self.message_queue.get()
            self.log(f"[WS] Broadcasting message to {len(self.clients)} clients")

            if not self.clients:
                continue

            # Parse message to check if ACK is required
            try:
                data = json.loads(msg)
                require_ack = data.get("require_ack", False)
                message_id = data.get("message_id")
            except:
                require_ack = False
                message_id = None

            remove_set = set()

            for client in list(self.clients):
                try:
                    await client.send(msg)

                    # Track message for ACK if required
                    if require_ack and message_id:
                        self.pending_messages[message_id] = {
                            "client": client,
                            "data": data,
                            "retries": 0,
                            "timestamp": time.time()
                        }

                except Exception:
                    remove_set.add(client)

            # Clean disconnected clients
            for c in remove_set:
                self.clients.discard(c)
                if c in self.client_info:
                    del self.client_info[c]

            self.log(f"[WS] Broadcast → {len(self.clients)} clients")

    # ------------------------------------------------------
    # Message handling and ACK mechanism
    # ------------------------------------------------------
    async def _handle_client_message(self, websocket, message):
        """Handle messages received from clients"""
        try:
            data = json.loads(message)

            # Handle ACK messages
            if data.get("type") == "ack" and "message_id" in data:
                message_id = data["message_id"]
                if message_id in self.pending_messages:
                    client_id = self.client_info.get(websocket, {}).get("id", "unknown")
                    self.log(f"[WS] Received ACK for message {message_id} from client {client_id}")
                    del self.pending_messages[message_id]
                return

            # Handle other message types
            self.log(f"[WS] Received from client: {message}")

        except json.JSONDecodeError:
            self.log(f"[WS] Invalid JSON from client: {message}")
        except Exception as e:
            self.log(f"[WS] Error handling client message: {e}")

    async def _stop_server(self):
        """Stop the server and close all connections"""
        # Close all clients
        for client in list(self.clients):
            try:
                await client.close()
            except:
                pass

        # Stop server
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        # Stop event loop
        self.loop.stop()

        self.log("[WS] Server stopped")


if __name__ == '__main__':
    def _input_loop(server: WebSocketServer):
        """Blocking CLI to send messages; type 'quit' to exit."""
        print("[WS] Input mode: type message to broadcast, or 'quit' to exit.")
        while True:
            try:
                text = input('> ').strip()
            except EOFError:
                # Ctrl-D
                text = 'quit'

            if not text:
                continue

            if text.lower() in ("quit", "exit", ":q", "q"):
                break

            # Broadcast plain text payload; clients can parse JSON if needed
            # Use ISO8601 UTC format for time (e.g., 2025-12-01T12:34:56.789Z)
            payload = {
                "type": "message",
                # Use timezone-aware UTC datetime (replacement for deprecated utcnow())
                "time": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
                "text": text,
            }
            server.broadcast(payload, require_ack=False)

        print("[WS] Exiting input mode...")

    try:
        # Initialize WebSocket server with ACK support
        websocket_server = WebSocketServer(
            host="0.0.0.0",
            port=8765,
            ack_timeout=5.0,
            max_retries=3,
            logger=logger,
        )
        websocket_server.start()

        # Run blocking input loop in main thread to "lock" the program
        _input_loop(websocket_server)

    except KeyboardInterrupt:
        print('\nShutting down...')
    finally:
        # Ensure server stops when leaving the input loop
        try:
            websocket_server.stop()
        except Exception:
            pass

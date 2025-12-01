#!/usr/bin/env python3
"""
簡單的 WebSocket 客戶端
可以連接到 WebSocket 服務器並發送消息
"""

import asyncio
import json
import websockets


async def simple_client():
    """簡單的 WebSocket 客戶端"""
    uri = "ws://0.0.0.0:8765"

    try:
        # 連接到 WebSocket 服務器
        async with websockets.connect(uri) as websocket:
            print(f"✓ 已連接到 {uri}")

            # 發送一個簡單的消息
            message = {
                "type": "message",
                "content": "Hello from client!"
            }

            await websocket.send(json.dumps(message))
            print(f"✓ 已發送消息: {message}")

            # 等待並接收回應
            while True:
                response = await websocket.recv()
                print(f"✓ 收到回應: {response}")
                data = json.loads(response)
                if data['text'] == "out":
                    print("✗ 收到退出指令，關閉連接")
                    break
    except ConnectionRefusedError:
        print("✗ 無法連接到服務器，請確保 WebSocket 服務器正在運行")
    except Exception as e:
        print(f"✗ 發生錯誤: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("簡單 WebSocket 客戶端")
    print("=" * 50)

    # 運行客戶端
    asyncio.run(simple_client())

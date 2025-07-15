import asyncio
import websockets

async def hello():
    uri = "wss://echo.websocket.org"  # 或你自己的 ws://server:port
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello WebSocket!")
        print("✅ Sent: Hello WebSocket!")

        response = await websocket.recv()
        print(f"📩 Received: {response}")

asyncio.run(hello())
print("Good !!")

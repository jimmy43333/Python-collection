# Python-Collecton

## Feature

- `lib/memory_monitor.py`：`MemoryMonitor` 類別 (核心邏輯)
- `main/memory_monitor.py`：命令列入口程式

## Install

```bash
# 1. 取得原始碼 (將 <repo-url> 換成實際 Git 倉庫網址)
git clone <repo-url>
cd Python-collection

# 2. 建立與啟用虛擬環境 (Linux / macOS)
python -m venv .venv
source .venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt
```

## Usage

#### memory_monitor.py

- 系統記憶體概況 (含 Swap)
- 列出記憶體使用量最高的前 N 個進程 (`-t`)
- 依 PID 監控單一進程 (`-p`)
- 依名稱關鍵字監控多個進程 (`-n`)，可與 `-t` 搭配只顯示前 N 個並列出總數
- 單次查詢 (`--once`) 或持續監控 (迴圈刷新)

```bash
python main/memory_monitor.py [選項]
```

- `-p, --pid <PID>`：監控指定 PID (與 `-n` 互斥)
- `-n, --name <字串>`：監控名稱包含該子字串的所有進程 (與 `-p` 互斥)
- `-i, --interval <秒>`：刷新間隔 (預設 1)
- `-t, --top <數量>`：顯示前 N 個記憶體使用量最高的進程 (預設 10；可為 0 表示不列出清單)
- `-s, --system`：系統模式 (顯示整體記憶體 + 前 N 個進程)
- `--once`：只執行一次後結束

###### Example

```bash
# 系統記憶體 + 前 10 個進程 (預設)
python main/memory_monitor.py

# 單次顯示系統記憶體 + 前 20 個進程
python main/memory_monitor.py -t 20 --once

# 持續系統監控 (每 5 秒) 只看前 15 個
python main/memory_monitor.py -s -i 5 -t 15

# 單次查看 PID 1234
python main/memory_monitor.py -p 1234 --once

# 持續監控 PID 1234 (每 2 秒)
python main/memory_monitor.py -p 1234 -i 2

# 名稱含 "chrome"，單次顯示前 8 個並含總數
python main/memory_monitor.py -n chrome -t 8 --once

# 持續監控名稱含 "python" 的進程 (每 3 秒，僅前 5 個)
python main/memory_monitor.py -n python -i 3 -t 5

# 列出名稱含 "node" 的進程 (預設前 10 個) 單次
python main/memory_monitor.py -n node --once

# 只顯示系統記憶體資訊 (不列出進程)
python main/memory_monitor.py -s --once -t 0
```

###### 注意事項

- `-p` 與 `-n` 互斥不可同時使用。
- 使用 `-n` 搭配 `-t` 時會同時顯示總匹配數與前 N 個進程。
- `--once` 適合快照或腳本整合，不會進入迴圈。
- 進程排序依 RSS (常駐集) 由大到小。

###### 輸出欄位

- `RSS`：常駐集大小 (物理記憶體)
- `VMS`：虛擬記憶體大小
- `百分比`：佔系統總記憶體比例
- `PID`：進程識別碼
- `狀態`：進程狀態 (running / sleeping 等)

#### websocket_server.py / websocket_client.py

簡單的 WebSocket 範例，提供一個可在背景執行的廣播伺服器與一個接收/發送訊息的客戶端。

###### 功能摘要

- 伺服器 (`socket/websocket_server.py`)
	- 後台 Thread 啟動 asyncio WebSocket 伺服器
	- 支援廣播訊息給所有已連線客戶端
	- 可選擇加上 `require_ack` 產生 `message_id`（目前僅送出，不含自動重送邏輯展示）
	- CLI 互動輸入：在主執行緒輸入文字即廣播
- 客戶端 (`socket/websocket_client.py`)
	- 連線到伺服器後先送出一則 JSON 訊息
	- 持續接收伺服器廣播並列印

###### 啟動伺服器

```bash
python socket/websocket_server.py
```

啟動後會顯示：

```
[WS] Server listening on ws://0.0.0.0:8765
[WS] Server thread started
[WS] Input mode: type message to broadcast, or 'quit' to exit.
>
```

在 `>` 提示符下輸入任意文字（例如 `hello`）就會廣播：

```
> hello
[WS] Broadcasting message to 1 clients
```

輸入 `quit` / `exit` / `q` 結束伺服器。

###### 啟動客戶端

於另一個終端視窗執行：

```bash
python socket/websocket_client.py
```

成功連線會看到：

```
==================================================
簡單 WebSocket 客戶端
==================================================
✓ 已連接到 ws://0.0.0.0:8765
✓ 已發送消息: {'type': 'message', 'content': 'Hello from client!'}
✓ 收到回應: {"type": "message", "time": "2025-12-01T12:34:56.789Z", "text": "hello"}
```

###### 範例廣播程式呼叫

若在其他程式中使用伺服器並以程式碼廣播：

```python
from socket.websocket_server import WebSocketServer

ws = WebSocketServer(port=8765)
ws.start()

ws.broadcast({"type": "message", "text": "from code"})
# 要求 ACK 的訊息
ws.broadcast({"type": "update", "payload": 123}, require_ack=True)
```

###### 注意事項

- 若出現 `ConnectionRefusedError`，確認伺服器已先啟動且使用相同 `host` / `port`。
- 廣播資料格式為 JSON 字串；客戶端可自行擴充解析不同 `type`。
- 目前 ACK 資料結構已建立，實際重送/超時機制可視需求延伸。
- 修改預設連線埠可在建立伺服器時指定 `port` 參數。
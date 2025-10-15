# Socket 工具說明

提供簡易 TCP Server 以及多種模式的 Client 測試工具。

## 檔案列表

- `simple_server.py`: 最簡易的 TCP 伺服器，回應收到的每行資料 (轉為大寫)。
- `simple_client.py`: 互動式或單次發送的 TCP 客戶端。
- `multi_client.py`: 多執行緒、多連線壓力/行為測試客户端，支援持久連線與每封包重連模式。

## simple_server.py 用法

```bash
python simple_server.py --ip 0.0.0.0 --port 5000
```

## simple_client.py 用法

互動模式:

```bash
python simple_client.py --ip 127.0.0.1 --port 5000
```

單次訊息:

```bash
python simple_client.py --ip 127.0.0.1 --port 5000 --message "hello"
```

輸入 `quit` 結束連線。

## multi_client.py 用法

```bash
python multi_client.py [--ip IP] [--port PORT] [--clients N] [--count M] [--message MSG] [--interval SEC] [--timeout SEC] [--mode MODE]
```

參數說明:

- `--ip`: 伺服器 IP，預設 127.0.0.1
- `--port`: 伺服器埠號，預設 5000
- `--clients`: 同時建立的執行緒/連線數量，預設 1
- `--count`: 每個連線要傳送的封包數量，設定 0 代表無限傳送直到中斷 (Ctrl+C)
- `--message`: 訊息前綴字串，實際送出格式為 `<prefix>-client<編號>-seq<序號>`，預設 hello
- `--interval`: 兩次送出間的睡眠秒數，預設 0.05 (可設 0)
- `--timeout`: 建立連線 (persistent) 或每次建立連線 (reconnect) 的逾時秒數，預設 5
- `--mode`: `persistent` 或 `reconnect`
  - `persistent`: 每個執行緒建立一次連線並重複傳送直至達到 count 或中斷
  - `reconnect`: 每一筆封包皆重新建立一次 socket 連線，送出後立即關閉

### 使用範例
1. 5 條持久連線，各自送 100 封包:
```bash
python multi_client.py --clients 5 --count 100 --message ping --interval 0.01 --mode persistent
```
2. 3 條持久連線無限傳送直到 Ctrl+C:
```bash
python multi_client.py --clients 3 --count 0 --message test --mode persistent
```
3. 2 條每封包重連模式，送 50 封包:
```bash
python multi_client.py --clients 2 --count 50 --message hi --mode reconnect --interval 0.005
```

### Log 與輸出
- 所有 socket 相關 log 會寫入 `logs/` 目錄:
  - `socket_server.log`
  - `socket_client.log`
  - `socket_multi_client.log`
- `multi_client.py` 結束時會在終端輸出 SUMMARY 包含 sent/recv/errors 總計。

### 中斷
按下 `Ctrl+C` 會觸發停止事件，等待所有執行緒收尾後印出 SUMMARY。

## 建議
- 若欲高壓測試，建議降低 `--interval` 或設為 0，但請注意 CPU 使用率。
- `reconnect` 模式會大量建立/關閉連線，可能受 OS 檔案描述符數量與 TIME_WAIT 影響，可視需要調整系統參數。

---
如需新增功能或更細緻監控 (如傳輸速率、失敗重試等) 可再提出需求。

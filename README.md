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
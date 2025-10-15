#!/usr/bin/env python3
"""
Process Memory Monitor - Main Entry Point
進程記憶體監控器 - 主程式入口
"""

import argparse
import sys
import os
from datetime import datetime  # 新增用於時間戳

# 添加父目錄到 Python 路徑，以便可以 import lib 模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.memory_monitor import MemoryMonitor


def main():
    """主函數 - 處理命令列參數並執行相應的監控功能"""
    parser = argparse.ArgumentParser(description="進程記憶體監控器")
    # 建立互斥參數組: -p 與 -n 互斥
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--pid', type=int, help="監控指定 PID 的進程")
    group.add_argument('-n', '--name', type=str, help="監控符合名稱(子字串)的進程")
    parser.add_argument('-i', '--interval', type=int, default=1, help="監控間隔 (秒)")
    parser.add_argument('-t', '--top', type=int, default=10, help="顯示記憶體使用量最高的進程數量")
    parser.add_argument('-s', '--system', action='store_true', help="監控整個系統")
    parser.add_argument('--once', action='store_true', help="只執行一次，不持續監控")

    args = parser.parse_args()

    # 創建記憶體監控器實例
    monitor = MemoryMonitor()

    try:
        if args.pid:
            if args.once:
                # 只查看一次指定進程的記憶體資訊
                process_info = monitor.get_process_memory_info(args.pid)
                monitor.print_process_info(process_info)
            else:
                # 持續監控指定進程
                monitor.monitor_process(args.pid, args.interval)
        elif args.name:
            if args.once:
                matched = monitor.get_processes_by_name(args.name)
                matched.sort(key=lambda p: p['memory_info'].rss, reverse=True)
                if args.top:
                    matched = matched[:args.top]
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{ts}] 名稱包含 '{args.name}' 的進程 (最多顯示 {args.top} 個):")
                if not matched:
                    print("未找到符合的進程")
                else:
                    for info in matched:
                        rss = info['memory_info'].rss
                        print(f"  PID {info['pid']:>6} | {info['name']:<20} | 記憶體: {monitor.format_bytes(rss):>10} ({info['memory_percent']:>5.1f}%)")
            else:
                monitor.monitor_process_by_name(args.name, args.interval, top_count=args.top)
        elif args.system:
            if args.once:
                # 只查看一次系統記憶體資訊
                monitor.get_system_memory_info()
                processes = monitor.get_all_processes_memory()
                monitor.print_top_processes(processes, args.top)
            else:
                # 持續監控系統記憶體使用情況
                monitor.monitor_system(args.interval, args.top)
        else:
            # 預設行為：顯示系統記憶體資訊和記憶體使用量最高的進程
            monitor.get_system_memory_info()
            processes = monitor.get_all_processes_memory()
            monitor.print_top_processes(processes, args.top)

    except KeyboardInterrupt:
        print("\n程式已被用戶中斷")
    except Exception as e:
        print(f"執行過程中發生錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

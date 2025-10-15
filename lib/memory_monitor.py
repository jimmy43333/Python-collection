#!/usr/bin/env python3
"""
Memory Monitor Library
記憶體監控庫
"""

import psutil
import time
from datetime import datetime


class MemoryMonitor:
    def __init__(self):
        self.processes = []

    def get_process_memory_info(self, pid):
        """獲取指定 PID 的記憶體資訊"""
        try:
            process = psutil.Process(pid)
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()

            return {
                'pid': pid,
                'name': process.name(),
                'rss': memory_info.rss,  # 實際記憶體使用量 (bytes)
                'vms': memory_info.vms,  # 虛擬記憶體使用量 (bytes)
                'percent': memory_percent,  # 記憶體使用百分比
                'status': process.status(),
                'create_time': datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None

    def get_all_processes_memory(self):
        """獲取所有進程的記憶體資訊"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent', 'status', 'create_time']):
            try:
                info = proc.info
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'rss': info['memory_info'].rss,
                    'vms': info['memory_info'].vms,
                    'percent': info['memory_percent'],
                    'status': info['status'],
                    'create_time': datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # 按記憶體使用量排序 (由高到低)
        return sorted(processes, key=lambda x: x['rss'], reverse=True)

    def format_bytes(self, bytes_value):
        """將 bytes 轉換為可讀格式"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"

    def print_process_info(self, process_info):
        """打印進程資訊"""
        if process_info is None:
            print("進程不存在或無法訪問")
            return

        print(f"PID: {process_info['pid']}")
        print(f"名稱: {process_info['name']}")
        print(f"實際記憶體 (RSS): {self.format_bytes(process_info['rss'])}")
        print(f"虛擬記憶體 (VMS): {self.format_bytes(process_info['vms'])}")
        print(f"記憶體百分比: {process_info['percent']:.2f}%")
        print(f"狀態: {process_info['status']}")
        print(f"創建時間: {process_info['create_time']}")
        print("-" * 50)

    def print_top_processes(self, processes, count=10):
        """打印記憶體使用量最高的進程"""
        print(f"\n記憶體使用量最高的 {count} 個進程:")
        print("=" * 80)
        print(f"{'PID':<8} {'名稱':<20} {'RSS':<12} {'VMS':<12} {'百分比':<8} {'狀態':<12}")
        print("-" * 80)

        for i, proc in enumerate(processes[:count]):
            print(f"{proc['pid']:<8} {proc['name'][:20]:<20} "
                  f"{self.format_bytes(proc['rss']):<12} "
                  f"{self.format_bytes(proc['vms']):<12} "
                  f"{proc['percent']:.1f}%{'':<3} {proc['status']:<12}")

    def get_system_memory_info(self):
        """獲取系統記憶體資訊"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        print("系統記憶體資訊:")
        print("=" * 50)
        print(f"總記憶體: {self.format_bytes(memory.total)}")
        print(f"可用記憶體: {self.format_bytes(memory.available)}")
        print(f"已使用記憶體: {self.format_bytes(memory.used)}")
        print(f"記憶體使用率: {memory.percent}%")
        print(f"交換空間總量: {self.format_bytes(swap.total)}")
        print(f"交換空間已使用: {self.format_bytes(swap.used)}")
        print(f"交換空間使用率: {swap.percent}%")
        print("=" * 50)

    def monitor_process(self, pid, interval=1):
        """持續監控指定進程"""
        print(f"開始監控 PID {pid} 的記憶體使用情況 (每 {interval} 秒更新一次)")
        print("按 Ctrl+C 停止監控")

        try:
            while True:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
                process_info = self.get_process_memory_info(pid)
                self.print_process_info(process_info)

                if process_info is None:
                    print("進程已結束或無法訪問，停止監控")
                    break

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n監控已停止")

    def monitor_system(self, interval=5, top_count=10):
        """持續監控系統記憶體使用情況"""
        print(f"開始監控系統記憶體使用情況 (每 {interval} 秒更新一次)")
        print("按 Ctrl+C 停止監控")

        try:
            while True:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
                self.get_system_memory_info()

                processes = self.get_all_processes_memory()
                self.print_top_processes(processes, top_count)

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n監控已停止")

    def get_processes_by_name(self, process_name):
        """取得符合名稱的所有進程資訊 (單次)"""
        matched = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    matched.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return matched

    def monitor_process_by_name(self, process_name, interval=2, top_count=None):
        """根據進程名稱持續監控記憶體, 可選擇只列出前 top_count 個，並顯示總匹配數"""
        print(f"監控進程名稱關鍵字: {process_name}")
        if top_count:
            print(f"每次僅顯示記憶體使用前 {top_count} 個符合的進程 (同時顯示總匹配數)")
        print("按 Ctrl+C 停止監控\n")

        try:
            while True:
                all_found = self.get_processes_by_name(process_name)
                total_found = len(all_found)
                # 依 RSS 由大到小排序
                all_found.sort(key=lambda p: p['memory_info'].rss, reverse=True)
                display_list = all_found
                if top_count:
                    display_list = all_found[:top_count]
                timestamp = datetime.now().strftime('%H:%M:%S')
                if total_found == 0:
                    print(f"[{timestamp}] 未找到進程: {process_name}")
                else:
                    if top_count and total_found > top_count:
                        print(f"[{timestamp}] 總共找到 {total_found} 個進程，顯示前 {len(display_list)} 個:")
                    else:
                        print(f"[{timestamp}] 找到 {total_found} 個進程:")
                    for proc in display_list:
                        rss = proc['memory_info'].rss
                        print(f"  PID {proc['pid']:>6} | {proc['name']:<20} | 記憶體: {self.format_bytes(rss):>10} ({proc['memory_percent']:>5.1f}%)")
                print()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("監控已停止")

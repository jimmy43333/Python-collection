#!/usr/bin/env python3
"""
Memory Monitor Library
記憶體監控庫
"""

import psutil
import time
from datetime import datetime
import csv
import os


class MemoryMonitor:
    def __init__(self):
        self.processes = []

    def get_process_memory_info(self, pid):
        """獲取指定 PID 的記憶體資訊"""
        try:
            process = psutil.Process(pid)
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            cmdline = process.cmdline() or []
            cmdline_join_lower = ' '.join(cmdline).lower()

            return {
                'pid': pid,
                'name': cmdline_join_lower,
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

    def get_processes_by_name(self, process_name):
        """取得符合名稱或命令列關鍵字的所有進程資訊 (單次)
        支援:
        - 可執行檔名稱 (如: python3)
        - 腳本檔名 (如: simple_server.py)
        - 命令列任意參數關鍵字
        回傳的 name 會在偵測到 .py 腳本時以腳本檔名取代，方便顯示。
        """
        keyword = process_name.lower()
        matched = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info', 'memory_percent']):
            try:
                info = proc.info
                cmdline = info.get('cmdline') or []
                name_lower = (info.get('name') or '').lower()
                cmdline_join_lower = ' '.join(cmdline).lower()

                # 是否匹配: 可執行檔名 / 任一參數 / 整體命令列
                if("memory_monitor.py" not in cmdline_join_lower):  # 忽略本程式
                    if (keyword in name_lower) or (keyword in cmdline_join_lower):
                        info['cmdline'] = cmdline_join_lower  # 用腳本檔名覆蓋顯示
                        matched.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return matched

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

    def monitor_process_log(self, pid, interval=1, log_file='monitor_pid.csv', log_interval=None):
        """僅寫入指定 PID 進程記憶體使用情況到 CSV (不輸出終端)
        第一行: cmdline,<完整命令列>
        第二行(表頭): timestamp,rss,vms,percent,status
        後續行: 寫入各次資料 (rss/vms 為人類可讀格式)
        會追蹤最大 rss / vms 並在結束時輸出。
        """
        if log_interval is None:
            log_interval = interval
        next_log_time = time.time()
        header = ['timestamp', 'rss', 'vms', 'percent', 'status']
        file_exists = os.path.exists(log_file) and os.path.getsize(log_file) > 0
        max_rss = 0
        max_vms = 0
        ended = False
        try:
            with open(log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    try:
                        proc_obj = psutil.Process(pid)
                        cmdline_list = proc_obj.cmdline() or []
                        cmdline_str = ' '.join(cmdline_list)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        cmdline_str = ''
                    writer.writerow(['cmdline', cmdline_str])
                    writer.writerow(header)
                while True:
                    now = time.time()
                    info = self.get_process_memory_info(pid)
                    if info is None:
                        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '', '', '', 'ENDED'])
                        f.flush()
                        ended = True
                        break
                    # 每 interval 更新最大值
                    if info['rss'] > max_rss:
                        max_rss = info['rss']
                    if info['vms'] > max_vms:
                        max_vms = info['vms']
                    # 達到 log_interval 時寫入
                    if now >= next_log_time:
                        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([ts, self.format_bytes(info['rss']), self.format_bytes(info['vms']), f"{info['percent']:.2f}", info['status']])
                        f.flush()
                        next_log_time = now + log_interval
                    time.sleep(interval)
        except KeyboardInterrupt:
            print("監控已停止")
        finally:
            # 直接讀取第一行並附加最大值資訊 (不重新取得 cmdline)
            summary_added = False
            try:
                with open(log_file, 'r+', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines and 'max_rss,' not in lines[0]:
                        lines[0] = lines[0].rstrip('\n') + f",max_rss,{self.format_bytes(max_rss)},max_vms,{self.format_bytes(max_vms)}\n"
                        f.seek(0)
                        f.writelines(lines)
                        f.truncate()
                        summary_added = True
            except Exception:
                pass
            print(f"PID {pid} 最大 RSS: {self.format_bytes(max_rss)} 最大 VMS: {self.format_bytes(max_vms)}" + (" (進程已結束)" if ended else "") + (" (已寫入檔案)" if summary_added else ""))

    def monitor_process_by_name_log(self, process_name, interval=2, top_count=None, log_file='monitor_name.csv', log_interval=None):
        """根據名稱/腳本關鍵字記錄符合的進程記憶體資訊到多個 CSV 檔 (不輸出終端)
        每個 PID 一個檔案: <PID>_<log_file>
        第一行: cmdline,<完整命令列>
        第二行(表頭): timestamp,rss,vms,percent,status
        後續行寫入資料，追蹤最大 rss / vms，Ctrl+C 時輸出所有 PID 最大值摘要。
        """
        if log_interval is None:
            log_interval = interval
        next_log_time = time.time()
        base_dir = os.path.dirname(log_file)
        base_name = os.path.basename(log_file)
        header = ['timestamp', 'rss', 'vms', 'percent', 'status']
        max_map = {}  # pid -> {'rss': int, 'vms': int}
        try:
            while True:
                now = time.time()
                all_found = self.get_processes_by_name(process_name)
                all_found.sort(key=lambda p: p['memory_info'].rss, reverse=True)
                display_list = all_found if not top_count else all_found[:top_count]
                # 每 interval 更新最大值
                for proc in display_list:
                    pid = proc['pid']
                    rss_b = proc['memory_info'].rss
                    # memory_info 可能有 vms
                    vms_b = getattr(proc['memory_info'], 'vms', 0)
                    if pid not in max_map:
                        max_map[pid] = {'rss': rss_b, 'vms': vms_b}
                    else:
                        if rss_b > max_map[pid]['rss']:
                            max_map[pid]['rss'] = rss_b
                        if vms_b > max_map[pid]['vms']:
                            max_map[pid]['vms'] = vms_b
                if now >= next_log_time:
                    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for proc in display_list:
                        pid = proc['pid']
                        rss_bytes = proc['memory_info'].rss
                        vms_bytes = getattr(proc['memory_info'], 'vms', 0)
                        try:
                            p_obj = psutil.Process(pid)
                            status = p_obj.status()
                            cmdline_list = p_obj.cmdline() or []
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            status = 'unknown'
                            cmdline_list = []
                        cmdline_str = ' '.join(cmdline_list)
                        per_file = os.path.join(base_dir, f"{pid}_{base_name}") if base_dir else f"{pid}_{base_name}"
                        file_exists = os.path.exists(per_file) and os.path.getsize(per_file) > 0
                        with open(per_file, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            if not file_exists:
                                writer.writerow(['cmdline', cmdline_str])
                                writer.writerow(header)
                            writer.writerow([ts, self.format_bytes(rss_bytes), self.format_bytes(vms_bytes), f"{proc['memory_percent']:.2f}", status])
                    next_log_time = now + log_interval
                time.sleep(interval)
        except KeyboardInterrupt:
            print("監控已停止")
        finally:
            print("最大記憶體使用摘要:")
            for pid, vals in sorted(max_map.items(), key=lambda x: x[1]['rss'], reverse=True):
                print(f"  PID {pid}: 最大 RSS {self.format_bytes(vals['rss'])} 最大 VMS {self.format_bytes(vals['vms'])}")
                per_file = os.path.join(base_dir, f"{pid}_{base_name}") if base_dir else f"{pid}_{base_name}"
                try:
                    if os.path.exists(per_file):
                        with open(per_file, 'r+', encoding='utf-8') as f:
                            lines = f.readlines()
                            if lines and 'max_rss,' not in lines[0]:
                                lines[0] = lines[0].rstrip('\n') + f",max_rss,{self.format_bytes(vals['rss'])},max_vms,{self.format_bytes(vals['vms'])}\n"
                                f.seek(0)
                                f.writelines(lines)
                                f.truncate()
                except Exception:
                    pass

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IoT蓝牙安全测试工具 - Windows主程序
IoT Bluetooth Security Testing Tool
毕业设计配套工具 - Windows版本
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, Menu
import threading
import json
import datetime
import os
import sys
from pathlib import Path

try:
    from bleak import BleakScanner
    HAS_BLEAK = True
except ImportError:
    HAS_BLEAK = False

# 简化：只使用BLE扫描，避免pybluez编译问题
HAS_PYBLUEZ = False


class BluetoothSecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT蓝牙安全测试工具 v1.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        self.devices = []
        self.scan_thread = None
        self.is_scanning = False
        
        self.setup_menu()
        self.create_widgets()
        
        self.log_message("工具已初始化")
        self.log_message(f"PyBluez: {'已安装' if HAS_PYBLUEZ else '未安装'}")
        self.log_message(f"Bleak: {'已安装' if HAS_BLEAK else '未安装'}")
    
    def setup_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导出报告", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        scan_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="扫描", menu=scan_menu)
        scan_menu.add_command(label="开始扫描", command=self.start_scan)
        scan_menu.add_command(label="停止扫描", command=self.stop_scan)
        scan_menu.add_separator()
        scan_menu.add_command(label="清空列表", command=self.clear_devices)
        
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
        help_menu.add_command(label="使用说明", command=self.show_help)
    
    def create_widgets(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#667eea", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="IoT蓝牙安全测试工具",
            font=("Microsoft YaHei", 24, "bold"),
            fg="white",
            bg="#667eea"
        )
        title_label.pack(pady=20)
        
        # 控制按钮区域
        control_frame = tk.Frame(self.root, bg="#f5f5f5")
        control_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(
            control_frame,
            text="🔍 开始扫描",
            command=self.start_scan,
            width=15,
            height=2,
            bg="#667eea",
            fg="white",
            font=("Microsoft YaHei", 10)
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="⏹ 停止扫描",
            command=self.stop_scan,
            width=15,
            height=2,
            bg="#ff6b6b",
            fg="white",
            font=("Microsoft YaHei", 10)
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="📊 安全评估",
            command=self.run_security_assessment,
            width=15,
            height=2,
            bg="#20c997",
            fg="white",
            font=("Microsoft YaHei", 10)
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="📄 生成报告",
            command=self.export_report,
            width=15,
            height=2,
            bg="#764ba2",
            fg="white",
            font=("Microsoft YaHei", 10)
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="🗑️ 清空列表",
            command=self.clear_devices,
            width=15,
            height=2,
            bg="#666666",
            fg="white",
            font=("Microsoft YaHei", 10)
        ).pack(side="left", padx=5)
        
        # 主内容区域
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 左侧：设备列表
        left_frame = tk.LabelFrame(main_frame, text="发现的设备", font=("Microsoft YaHei", 12))
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        columns = ("name", "address", "type", "rssi", "risk")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("name", text="设备名称")
        self.tree.heading("address", text="MAC地址")
        self.tree.heading("type", text="类型")
        self.tree.heading("rssi", text="信号强度")
        self.tree.heading("risk", text="风险等级")
        
        self.tree.column("name", width=200)
        self.tree.column("address", width=150)
        self.tree.column("type", width=80)
        self.tree.column("rssi", width=80)
        self.tree.column("risk", width=80)
        
        scrollbar_y = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(left_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_device_select)
        
        # 右侧：详细信息
        right_frame = tk.LabelFrame(main_frame, text="设备详情", font=("Microsoft YaHei", 12))
        right_frame.pack(side="right", fill="both", expand=True)
        
        self.detail_text = scrolledtext.ScrolledText(
            right_frame,
            width=40,
            height=15,
            font=("Consolas", 10)
        )
        self.detail_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 日志区域
        log_frame = tk.LabelFrame(self.root, text="操作日志", font=("Microsoft YaHei", 12))
        log_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, font=("Consolas", 9))
        self.log_text.pack(fill="x", padx=10, pady=10)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 - 点击'开始扫描'开始扫描蓝牙设备")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor="w",
            bg="#667eea",
            fg="white"
        )
        status_bar.pack(side="bottom", fill="x")
    
    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def start_scan(self):
        if self.is_scanning:
            self.log_message("扫描已在进行中...")
            return
        
        self.is_scanning = True
        self.log_message("开始扫描...")
        self.status_var.set("正在扫描...")
        
        self.scan_thread = threading.Thread(target=self.scan_devices, daemon=True)
        self.scan_thread.start()
    
    def scan_devices(self):
        try:
            if HAS_PYBLUEZ:
                self.log_message("扫描经典蓝牙设备...")
                nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
                
                for addr, name in nearby_devices:
                    self.root.after(0, lambda a=addr, n=name: self.add_device(a, n, "Classic Bluetooth"))
            
            if HAS_BLEAK:
                self.log_message("扫描BLE设备...")
                ble_devices = await BleakScanner.discover(timeout=8)
                
                for device in ble_devices:
                    self.root.after(0, lambda d=device: self.add_device(d.address, d.name or "Unknown", "BLE"))
            
            if not HAS_PYBLUEZ and not HAS_BLEAK:
                self.log_message("警告：未安装蓝牙库，使用模拟数据")
                self.simulate_devices()
            
        except Exception as e:
            self.log_message(f"扫描出错：{str(e)}")
        finally:
            self.is_scanning = False
            self.root.after(0, lambda: self.status_var.set(f"扫描完成 - 发现 {len(self.devices)} 个设备"))
            self.root.after(0, lambda: self.log_message("扫描完成"))
    
    def simulate_devices(self):
        mock_devices = [
            ("AA:BB:CC:DD:EE:01", "ESP32-Test-Device", "BLE", -45),
            ("AA:BB:CC:DD:EE:02", "Raspberry-Pi-4", "Classic Bluetooth", -60),
            ("AA:BB:CC:DD:EE:03", "Smart-Band-X", "BLE", -55),
            ("00:00:00:11:22:33", "Default-Device", "Classic Bluetooth", -70),
            ("AA:BB:CC:DD:EE:05", "IoT-Sensor-01", "BLE", -50),
        ]
        
        for addr, name, dtype, rssi in mock_devices:
            self.root.after(0, lambda a=addr, n=name, t=dtype, r=rssi: self.add_device(a, n, t, r))
            import time
            time.sleep(0.5)
    
    def add_device(self, address, name, device_type, rssi=-60):
        risk = self.evaluate_risk(name, address)
        
        device_info = {
            "name": name,
            "address": address,
            "type": device_type,
            "rssi": rssi,
            "risk": risk["level"],
            "score": risk["score"],
            "issues": risk["issues"]
        }
        
        self.devices.append(device_info)
        self.tree.insert("", "end", values=(
            name,
            address,
            device_type,
            f"{rssi} dBm" if rssi else "N/A",
            risk["level"]
        ))
        
        self.log_message(f"发现设备: {name} ({address})")
    
    def evaluate_risk(self, name, address):
        score = 0
        issues = []
        
        name_lower = name.lower() if name else ""
        
        if "admin" in name_lower or "root" in name_lower:
            score += 3
            issues.append("设备名称包含管理员相关词汇")
        
        if "test" in name_lower or "default" in name_lower:
            score += 2
            issues.append("可能使用默认名称")
        
        if "guest" in name_lower or "public" in name_lower:
            score += 2
            issues.append("可能为公共设备")
        
        if address.startswith("00:00:00"):
            score += 3
            issues.append("使用默认MAC地址")
        
        if score >= 7:
            level = "🔴 高风险"
        elif score >= 4:
            level = "🟡 中风险"
        elif score >= 2:
            level = "🟢 低风险"
        else:
            level = "✅ 安全"
        
        return {"level": level, "score": score, "issues": issues}
    
    def on_device_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]
            address = values[1]
            
            device = next((d for d in self.devices if d["address"] == address), None)
            if device:
                self.show_device_details(device)
    
    def show_device_details(self, device):
        details = f"""设备详情
{'='*50}

设备名称: {device['name']}
MAC地址:  {device['address']}
设备类型: {device['type']}
信号强度: {device['rssi']}
风险等级: {device['risk']}
安全评分: {device['score']}/10

风险分析:
"""
        if device['issues']:
            for issue in device['issues']:
                details += f"• {issue}\n"
        else:
            details += "• 未发现明显风险\n"
        
        details += f"""
安全建议:
• 只与可信设备配对
• 使用强配对密码
• 关闭不必要的可见性
• 定期检查配对设备
• 保持系统和驱动更新
"""
        
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, details)
    
    def stop_scan(self):
        if self.is_scanning:
            self.is_scanning = False
            self.log_message("正在停止扫描...")
            self.status_var.set("扫描已停止")
    
    def clear_devices(self):
        self.devices.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.detail_text.delete(1.0, tk.END)
        self.log_message("列表已清空")
    
    def run_security_assessment(self):
        if not self.devices:
            messagebox.showwarning("警告", "请先扫描设备！")
            return
        
        total = len(self.devices)
        high_risk = sum(1 for d in self.devices if "高风险" in d["risk"])
        medium_risk = sum(1 for d in self.devices if "中风险" in d["risk"])
        
        assessment = f"""安全评估报告
{'='*50}

扫描设备总数: {total}
高风险设备:   {high_risk}
中风险设备:   {medium_risk}
低风险/安全:  {total - high_risk - medium_risk}

整体安全状态: {'⚠️ 需要关注' if high_risk > 0 else '✅ 基本安全'}

建议措施:
1. 立即处理高风险设备
2. 评估中风险设备的必要性
3. 审查所有蓝牙设备的配对记录
4. 考虑使用蓝牙防火墙
5. 制定蓝牙使用安全策略
"""
        
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, assessment)
        self.log_message("安全评估完成")
    
    def export_report(self):
        if not self.devices:
            messagebox.showwarning("警告", "没有数据可导出！")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON文件", "*.json"),
                ("HTML文件", "*.html"),
                ("文本文件", "*.txt")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    self.export_json(filename)
                elif filename.endswith('.html'):
                    self.export_html(filename)
                else:
                    self.export_text(filename)
                
                messagebox.showinfo("成功", f"报告已保存至：{filename}")
                self.log_message(f"报告已导出：{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败：{str(e)}")
    
    def export_json(self, filename):
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_devices": len(self.devices),
            "devices": self.devices
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    
    def export_html(self, filename):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>蓝牙安全测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #667eea; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #667eea; color: white; }}
        .high {{ color: red; font-weight: bold; }}
        .medium {{ color: orange; }}
        .low {{ color: green; }}
    </style>
</head>
<body>
    <h1>IoT蓝牙安全测试报告</h1>
    <p>生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>设备总数: {len(self.devices)}</p>
    
    <h2>设备列表</h2>
    <table>
        <tr>
            <th>设备名称</th>
            <th>MAC地址</th>
            <th>类型</th>
            <th>风险等级</th>
        </tr>
"""
        for d in self.devices:
            risk_class = "high" if "高风险" in d["risk"] else "medium" if "中风险" in d["risk"] else "low"
            html += f"""        <tr>
            <td>{d['name']}</td>
            <td>{d['address']}</td>
            <td>{d['type']}</td>
            <td class="{risk_class}">{d['risk']}</td>
        </tr>
"""
        
        html += """    </table>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def export_text(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("IoT蓝牙安全测试报告\n")
            f.write(f"{'='*50}\n")
            f.write(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"设备总数: {len(self.devices)}\n\n")
            
            for i, d in enumerate(self.devices, 1):
                f.write(f"设备 #{i}\n")
                f.write(f"  名称: {d['name']}\n")
                f.write(f"  MAC:  {d['address']}\n")
                f.write(f"  类型: {d['type']}\n")
                f.write(f"  风险: {d['risk']}\n\n")
    
    def show_about(self):
        messagebox.showinfo(
            "关于",
            "IoT蓝牙安全测试工具 v1.0\n\n"
            "毕业设计配套工具\n"
            "赣州职业技术学院 信息安全2312班\n\n"
            "功能：\n"
            "• 蓝牙设备扫描\n"
            "• 安全风险评估\n"
            "• 漏洞检测\n"
            "• 报告生成\n\n"
            "仅供学习研究使用"
        )
    
    def show_help(self):
        help_text = """使用说明

1. 开始扫描
   - 点击"开始扫描"按钮
   - 等待扫描完成
   - 设备将显示在列表中

2. 查看详情
   - 点击列表中的设备
   - 右侧显示详细信息

3. 安全评估
   - 扫描完成后点击"安全评估"
   - 查看整体安全状态

4. 导出报告
   - 点击"生成报告"
   - 选择保存格式和位置

注意事项：
• 需要蓝牙适配器
• 部分功能需要管理员权限
• 仅用于授权的安全测试
"""
        messagebox.showinfo("使用说明", help_text)


def main():
    root = tk.Tk()
    app = BluetoothSecurityApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

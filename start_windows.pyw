#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnswerCustomer Windows 启动脚本
可以直接双击运行，不会显示控制台窗口
"""

import os
import sys
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import webbrowser
import time

class AnswerCustomerLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AnswerCustomer 启动器")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        self.setup_ui()
        self.server_process = None
        self.server_port = None
        
    def setup_ui(self):
        """设置用户界面"""
        # 标题
        title_label = tk.Label(self.root, text="🚀 AnswerCustomer 启动器", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="准备启动...", 
                                    font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # 日志显示区域
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_label = tk.Label(log_frame, text="启动日志:")
        log_label.pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="启动服务", 
                                     command=self.start_server, 
                                     bg="#4CAF50", fg="white", 
                                     font=("Arial", 10, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="停止服务", 
                                    command=self.stop_server, 
                                    bg="#f44336", fg="white", 
                                    font=("Arial", 10, "bold"),
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.open_browser_button = tk.Button(button_frame, text="打开浏览器", 
                                            command=self.open_browser, 
                                            bg="#2196F3", fg="white", 
                                            font=("Arial", 10, "bold"),
                                            state=tk.DISABLED)
        self.open_browser_button.pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.StringVar()
        self.progress_label = tk.Label(self.root, textvariable=self.progress_var)
        self.progress_label.pack(pady=5)
        
    def log(self, message):
        """添加日志信息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def check_python(self):
        """检查Python环境"""
        self.log("📋 检查Python环境...")
        self.status_label.config(text="检查Python环境...")
        
        if sys.version_info < (3, 7):
            self.log("❌ Python版本过低，需要Python 3.7或更高版本")
            messagebox.showerror("错误", "Python版本过低，需要Python 3.7或更高版本")
            return False
            
        self.log(f"✅ Python版本: {sys.version}")
        return True
        
    def check_pip(self):
        """检查pip"""
        self.log("📦 检查pip...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, check=True)
            self.log("✅ pip可用")
            return True
        except:
            self.log("❌ pip不可用")
            messagebox.showerror("错误", "pip不可用，请检查Python安装")
            return False
            
    def install_requirements(self):
        """安装依赖"""
        self.log("📥 安装项目依赖...")
        self.status_label.config(text="安装依赖...")
        
        if not os.path.exists("requirements.txt"):
            self.log("❌ requirements.txt文件不存在")
            messagebox.showerror("错误", "requirements.txt文件不存在")
            return False
            
        try:
            # 升级pip
            self.log("   - 升级pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                          capture_output=True, check=True)
            
            # 安装依赖
            self.log("   - 安装项目依赖...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ 依赖安装成功")
                return True
            else:
                self.log(f"❌ 依赖安装失败: {result.stderr}")
                messagebox.showerror("错误", f"依赖安装失败:\n{result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ 安装过程中发生错误: {e}")
            messagebox.showerror("错误", f"安装过程中发生错误:\n{e}")
            return False
            
    def create_directories(self):
        """创建数据目录"""
        self.log("📁 创建数据目录...")
        
        directories = ["data", "data/csv", "data/config"]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                self.log(f"   ✅ 创建目录: {directory}")
            except Exception as e:
                self.log(f"   ❌ 创建目录失败 {directory}: {e}")
                return False
                
        return True
        
    def find_port(self):
        """查找可用端口"""
        import socket
        
        for port in range(5000, 5010):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.server_port = port
                    self.log(f"✅ 找到可用端口: {port}")
                    return True
            except OSError:
                continue
                
        self.log("❌ 无法找到可用端口")
        return False
        
    def start_server(self):
        """启动服务器"""
        def start_thread():
            try:
                # 检查环境
                if not self.check_python():
                    return
                if not self.check_pip():
                    return
                if not self.install_requirements():
                    return
                if not self.create_directories():
                    return
                if not self.find_port():
                    return
                    
                # 启动服务器
                self.log(f"🚀 启动服务器 (端口: {self.server_port})...")
                self.status_label.config(text=f"启动服务器 (端口: {self.server_port})...")
                
                # 设置环境变量
                env = os.environ.copy()
                env['FLASK_APP'] = 'run.py'
                env['FLASK_ENV'] = 'development'
                
                # 启动服务器进程
                cmd = [sys.executable, "run.py", "--port", str(self.server_port)]
                self.server_process = subprocess.Popen(cmd, env=env, 
                                                     stdout=subprocess.PIPE, 
                                                     stderr=subprocess.PIPE,
                                                     text=True)
                
                # 等待服务器启动
                time.sleep(3)
                
                if self.server_process.poll() is None:
                    self.log("✅ 服务器启动成功")
                    self.status_label.config(text=f"服务器运行中 (端口: {self.server_port})")
                    
                    # 更新按钮状态
                    self.start_button.config(state=tk.DISABLED)
                    self.stop_button.config(state=tk.NORMAL)
                    self.open_browser_button.config(state=tk.NORMAL)
                    
                    # 自动打开浏览器
                    self.open_browser()
                    
                    # 监控服务器进程
                    self.monitor_server()
                else:
                    self.log("❌ 服务器启动失败")
                    messagebox.showerror("错误", "服务器启动失败")
                    
            except Exception as e:
                self.log(f"❌ 启动过程中发生错误: {e}")
                messagebox.showerror("错误", f"启动过程中发生错误:\n{e}")
                
        # 在新线程中启动服务器
        threading.Thread(target=start_thread, daemon=True).start()
        
    def monitor_server(self):
        """监控服务器进程"""
        def monitor():
            while self.server_process and self.server_process.poll() is None:
                time.sleep(1)
                
            if self.server_process:
                self.log("🛑 服务器已停止")
                self.status_label.config(text="服务器已停止")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.open_browser_button.config(state=tk.DISABLED)
                
        threading.Thread(target=monitor, daemon=True).start()
        
    def stop_server(self):
        """停止服务器"""
        if self.server_process:
            self.log("🛑 正在停止服务器...")
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
            
    def open_browser(self):
        """打开浏览器"""
        if self.server_port:
            url = f"http://localhost:{self.server_port}"
            self.log(f"🌐 打开浏览器: {url}")
            try:
                webbrowser.open(url)
            except Exception as e:
                self.log(f"❌ 打开浏览器失败: {e}")
                
    def run(self):
        """运行启动器"""
        self.root.mainloop()

def main():
    """主函数"""
    launcher = AnswerCustomerLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 
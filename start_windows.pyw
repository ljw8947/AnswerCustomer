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
        self.root.title("AnswerCustomer Launcher")
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
        title_label = tk.Label(self.root, text="🚀 AnswerCustomer Launcher", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="Preparing to start...", 
                                    font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # 日志显示区域
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_label = tk.Label(log_frame, text="Startup Log:")
        log_label.pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Server", 
                                     command=self.start_server, 
                                     bg="#4CAF50", fg="white", 
                                     font=("Arial", 10, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Server", 
                                    command=self.stop_server, 
                                    bg="#f44336", fg="white", 
                                    font=("Arial", 10, "bold"),
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.open_browser_button = tk.Button(button_frame, text="Open Browser", 
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
        """Add log message"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def check_python(self):
        """Check Python environment"""
        self.log("📋 Checking Python environment...")
        self.status_label.config(text="Checking Python environment...")
        if sys.version_info < (3, 7):
            self.log("❌ Python version too low, Python 3.7 or higher is required.")
            messagebox.showerror("Error", "Python version too low, Python 3.7 or higher is required.")
            return False
        self.log(f"✅ Python version: {sys.version}")
        return True
        
    def check_pip(self):
        """Check pip"""
        self.log("📦 Checking pip...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, check=True)
            self.log("✅ pip is available")
            return True
        except:
            self.log("❌ pip is not available")
            messagebox.showerror("Error", "pip is not available, please check your Python installation.")
            return False
            
    def install_requirements(self):
        """Install dependencies"""
        self.log("�� Installing project dependencies...")
        self.status_label.config(text="Installing dependencies...")
        if not os.path.exists("requirements.txt"):
            self.log("❌ requirements.txt file not found")
            messagebox.showerror("Error", "requirements.txt file not found")
            return False
            
        try:
            # Upgrade pip
            self.log("   - Upgrading pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                          capture_output=True, check=True)
            
            # Install dependencies
            self.log("   - Installing project dependencies...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Dependencies installed successfully")
                return True
            else:
                self.log(f"❌ Dependency installation failed: {result.stderr}")
                messagebox.showerror("Error", f"Dependency installation failed:\n{result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error occurred during installation: {e}")
            messagebox.showerror("Error", f"Error occurred during installation:\n{e}")
            return False
            
    def create_directories(self):
        """Create data directories"""
        self.log("📁 Creating data directories...")
        
        directories = ["data", "data/csv", "data/config"]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                self.log(f"   ✅ Created directory: {directory}")
            except Exception as e:
                self.log(f"   ❌ Failed to create directory {directory}: {e}")
                return False
                
        return True
        
    def find_port(self):
        """Find available port"""
        import socket
        
        for port in range(5000, 5010):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.server_port = port
                    self.log(f"✅ Found available port: {port}")
                    return True
            except OSError:
                continue
                
        self.log("❌ No available port found")
        return False
        
    def start_server(self):
        """Start server"""
        def start_thread():
            try:
                # Check environment
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
                    
                # Start server
                self.log(f"🚀 Starting server (port: {self.server_port})...")
                self.status_label.config(text=f"Starting server (port: {self.server_port})...")
                
                # Set environment variables
                env = os.environ.copy()
                env['FLASK_APP'] = 'run.py'
                env['FLASK_ENV'] = 'development'
                
                # Start server process
                cmd = [sys.executable, "run.py", "--port", str(self.server_port)]
                self.server_process = subprocess.Popen(cmd, env=env, 
                                                     stdout=subprocess.PIPE, 
                                                     stderr=subprocess.PIPE,
                                                     text=True)
                
                # Wait for server to start
                time.sleep(3)
                
                if self.server_process.poll() is None:
                    self.log("✅ Server started successfully")
                    self.status_label.config(text=f"Server running (port: {self.server_port})")
                    
                    # Update button state
                    self.start_button.config(state=tk.DISABLED)
                    self.stop_button.config(state=tk.NORMAL)
                    self.open_browser_button.config(state=tk.NORMAL)
                    
                    # Automatically open browser
                    self.open_browser()
                    
                    # Monitor server process
                    self.monitor_server()
                else:
                    self.log("❌ Server start failed")
                    messagebox.showerror("Error", "Server start failed")
                    
            except Exception as e:
                self.log(f"❌ Error occurred during start: {e}")
                messagebox.showerror("Error", f"Error occurred during start:\n{e}")
                
        # Start server in new thread
        threading.Thread(target=start_thread, daemon=True).start()
        
    def monitor_server(self):
        """监控服务器进程"""
        def monitor():
            while self.server_process and self.server_process.poll() is None:
                time.sleep(1)
                
            if self.server_process:
                self.log("🛑 Server stopped")
                self.status_label.config(text="Server stopped")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.open_browser_button.config(state=tk.DISABLED)
                
        threading.Thread(target=monitor, daemon=True).start()
        
    def stop_server(self):
        """停止服务器"""
        if self.server_process:
            self.log("🛑 Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
            
    def open_browser(self):
        """打开浏览器"""
        if self.server_port:
            url = f"http://localhost:{self.server_port}"
            self.log(f"🌐 Opening browser: {url}")
            try:
                webbrowser.open(url)
            except Exception as e:
                self.log(f"❌ Opening browser failed: {e}")
                
    def run(self):
        """运行启动器"""
        self.root.mainloop()

def main():
    """主函数"""
    launcher = AnswerCustomerLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnswerCustomer 初始化脚本
支持 macOS 和 Windows 平台
自动安装依赖并启动服务
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🚀 AnswerCustomer 初始化脚本")
    print("=" * 60)
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    print("=" * 60)

def check_python_version():
    """检查Python版本"""
    print("📋 检查Python版本...")
    if sys.version_info < (3, 7):
        print("❌ Python版本过低，需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def check_pip():
    """检查pip是否可用"""
    print("📦 检查pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip可用")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip不可用")
        return False

def install_requirements():
    """安装项目依赖"""
    print("📥 安装项目依赖...")
    
    # 检查requirements.txt是否存在
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt文件不存在")
        return False
    
    try:
        # 升级pip
        print("   - 升级pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # 安装依赖
        print("   - 安装项目依赖...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 依赖安装成功")
            return True
        else:
            print(f"❌ 依赖安装失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 安装过程中发生错误: {e}")
        return False

def create_data_directories():
    """创建必要的数据目录"""
    print("📁 创建数据目录...")
    
    directories = [
        "data",
        "data/csv",
        "data/config"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ 创建目录: {directory}")
        except Exception as e:
            print(f"   ❌ 创建目录失败 {directory}: {e}")
            return False
    
    return True

def check_port_availability(port=5000):
    """检查端口是否可用"""
    print(f"🔍 检查端口 {port} 可用性...")
    
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            print(f"✅ 端口 {port} 可用")
            return True
    except OSError:
        print(f"⚠️ 端口 {port} 被占用，将尝试其他端口")
        return False

def find_available_port(start_port=5000, max_attempts=10):
    """查找可用端口"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    return None

def start_server(port=5000):
    """启动Flask服务器"""
    print(f"🚀 启动服务器 (端口: {port})...")
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['FLASK_APP'] = 'run.py'
        env['FLASK_ENV'] = 'development'
        
        # 启动服务器
        cmd = [sys.executable, "run.py"]
        if port != 5000:
            cmd.extend(["--port", str(port)])
        
        print(f"   启动命令: {' '.join(cmd)}")
        print(f"   访问地址: http://localhost:{port}")
        print("   💡 按 Ctrl+C 停止服务器")
        print("-" * 60)
        
        # 启动服务器进程
        process = subprocess.Popen(cmd, env=env)
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 收到停止信号，正在关闭服务器...")
            process.terminate()
            process.wait()
            print("✅ 服务器已停止")
        
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print_banner()
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查pip
    if not check_pip():
        print("请先安装pip")
        sys.exit(1)
    
    # 安装依赖
    if not install_requirements():
        print("依赖安装失败，请检查网络连接或手动安装")
        sys.exit(1)
    
    # 创建数据目录
    if not create_data_directories():
        print("数据目录创建失败")
        sys.exit(1)
    
    # 查找可用端口
    port = find_available_port()
    if port is None:
        print("❌ 无法找到可用端口")
        sys.exit(1)
    
    # 启动服务器
    start_server(port)

if __name__ == "__main__":
    main() 
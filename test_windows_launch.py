#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Windows启动功能
"""

import os
import sys
import subprocess
import platform
import time
import socket

def test_python_environment():
    """测试Python环境"""
    print("🔍 测试Python环境...")
    
    # 检查Python版本
    version = sys.version_info
    print(f"   Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 7):
        print("   ❌ Python版本过低，需要3.7或更高版本")
        return False
    else:
        print("   ✅ Python版本符合要求")
    
    # 检查pip
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print("   ✅ pip可用")
        return True
    except:
        print("   ❌ pip不可用")
        return False

def test_requirements():
    """测试依赖安装"""
    print("📦 测试依赖安装...")
    
    if not os.path.exists("requirements.txt"):
        print("   ❌ requirements.txt不存在")
        return False
    
    try:
        # 尝试安装一个依赖包
        result = subprocess.run([sys.executable, "-m", "pip", "install", "flask"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ 依赖安装测试通过")
            return True
        else:
            print(f"   ❌ 依赖安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ 依赖安装异常: {e}")
        return False

def test_port_availability():
    """测试端口可用性"""
    print("🔌 测试端口可用性...")
    
    available_ports = []
    for port in range(5000, 5010):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                available_ports.append(port)
                print(f"   ✅ 端口 {port} 可用")
        except OSError:
            print(f"   ❌ 端口 {port} 被占用")
    
    if available_ports:
        print(f"   ✅ 找到可用端口: {available_ports[0]}")
        return available_ports[0]
    else:
        print("   ❌ 没有可用端口")
        return None

def test_file_structure():
    """测试文件结构"""
    print("📁 测试文件结构...")
    
    required_files = [
        "run.py",
        "config.py", 
        "requirements.txt",
        "app/__init__.py",
        "app/routes/admin.py",
        "app/routes/engineer.py",
        "app/routes/auth.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"   ❌ 缺少文件: {missing_files}")
        return False
    else:
        print("   ✅ 所有必需文件都存在")
        return True

def test_startup_script():
    """测试启动脚本"""
    print("🚀 测试启动脚本...")
    
    # 测试批处理脚本
    if os.path.exists("start_windows.bat"):
        print("   ✅ start_windows.bat 存在")
    else:
        print("   ❌ start_windows.bat 不存在")
    
    # 测试图形界面启动器
    if os.path.exists("start_windows.pyw"):
        print("   ✅ start_windows.pyw 存在")
    else:
        print("   ❌ start_windows.pyw 不存在")
    
    # 测试可执行文件生成器
    if os.path.exists("create_windows_exe.py"):
        print("   ✅ create_windows_exe.py 存在")
    else:
        print("   ❌ create_windows_exe.py 不存在")
    
    return True

def test_data_directories():
    """测试数据目录"""
    print("📂 测试数据目录...")
    
    directories = ["data", "data/csv", "data/config"]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ 目录 {directory} 创建成功")
        except Exception as e:
            print(f"   ❌ 目录 {directory} 创建失败: {e}")
            return False
    
    return True

def test_flask_app():
    """测试Flask应用"""
    print("🌐 测试Flask应用...")
    
    try:
        # 尝试导入Flask应用
        sys.path.insert(0, os.getcwd())
        from app import create_app
        
        app = create_app()
        print("   ✅ Flask应用创建成功")
        
        # 测试路由
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200 or response.status_code == 302:
                print("   ✅ 路由测试通过")
                return True
            else:
                print(f"   ❌ 路由测试失败: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Flask应用测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🪟 Windows启动功能测试")
    print("=" * 60)
    print()
    
    tests = [
        ("Python环境", test_python_environment),
        ("文件结构", test_file_structure),
        ("依赖安装", test_requirements),
        ("数据目录", test_data_directories),
        ("端口可用性", test_port_availability),
        ("启动脚本", test_startup_script),
        ("Flask应用", test_flask_app),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！Windows启动功能正常")
        print("\n📋 启动方式:")
        print("1. 双击 start_windows.bat")
        print("2. 双击 start_windows.pyw")
        print("3. 运行 python create_windows_exe.py 创建可执行文件")
    else:
        print("⚠️ 部分测试失败，请检查相关配置")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
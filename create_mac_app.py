#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建macOS应用程序包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_mac_app():
    """创建macOS应用程序包"""
    print("🍎 创建macOS应用程序包...")
    
    app_name = "AnswerCustomer.app"
    app_path = Path(app_name)
    
    # 如果已存在，先删除
    if app_path.exists():
        shutil.rmtree(app_path)
    
    # 创建应用程序包结构
    contents_path = app_path / "Contents"
    macos_path = contents_path / "MacOS"
    resources_path = contents_path / "Resources"
    
    os.makedirs(macos_path, exist_ok=True)
    os.makedirs(resources_path, exist_ok=True)
    
    # 创建Info.plist
    info_plist = contents_path / "Info.plist"
    info_plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>AnswerCustomer</string>
    <key>CFBundleIdentifier</key>
    <string>com.answercustomer.app</string>
    <key>CFBundleName</key>
    <string>AnswerCustomer</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
    
    with open(info_plist, 'w', encoding='utf-8') as f:
        f.write(info_plist_content)
    
    # 创建启动脚本
    launcher_script = macos_path / "AnswerCustomer"
    launcher_content = '''#!/bin/bash

# 获取应用程序包所在目录
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$APP_DIR"

# 检查Python
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python3未安装，请先安装Python 3.7或更高版本" buttons {"确定"} default button "确定"'
    exit 1
fi

# 运行初始化脚本
python3 init_and_run.py

# 如果启动失败，显示错误对话框
if [ $? -ne 0 ]; then
    osascript -e 'display dialog "启动失败，请检查错误信息" buttons {"确定"} default button "确定"'
fi
'''
    
    with open(launcher_script, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # 设置执行权限
    os.chmod(launcher_script, 0o755)
    
    # 复制项目文件到Resources目录
    project_files = [
        'app', 'config.py', 'run.py', 'init_and_run.py', 
        'requirements.txt', 'README.md', 'CHANGELOG.md'
    ]
    
    for file_path in project_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.copytree(file_path, resources_path / file_path)
            else:
                shutil.copy2(file_path, resources_path)
    
    print(f"✅ 应用程序包创建成功: {app_name}")
    print(f"   位置: {app_path.absolute()}")
    print("   现在可以双击运行了！")
    
    return app_path

if __name__ == "__main__":
    create_mac_app() 
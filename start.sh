#!/bin/bash

# AnswerCustomer 启动脚本 (macOS/Linux)

echo "============================================================"
echo "🚀 AnswerCustomer 启动脚本 (macOS/Linux)"
echo "============================================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    echo "请先安装Python 3.7或更高版本"
    echo "macOS: brew install python3"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✅ Python3已安装"
echo

# 检查脚本是否可执行
if [ ! -x "init_and_run.py" ]; then
    echo "🔧 设置脚本执行权限..."
    chmod +x init_and_run.py
fi

# 运行初始化脚本
echo "正在启动AnswerCustomer..."
python3 init_and_run.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ 启动失败，请检查错误信息"
    exit 1
fi 
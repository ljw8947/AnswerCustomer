@echo off
chcp 65001 >nul
title AnswerCustomer

echo.
echo ========================================
echo    AnswerCustomer 启动器
echo ========================================
echo.

:: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python
    pause
    exit /b 1
)

:: 安装依赖
echo 📦 安装依赖...
python -m pip install -r requirements.txt

:: 启动服务器
echo 🚀 启动服务器...
python run.py

pause 
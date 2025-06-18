@echo off
chcp 65001 >nul
title AnswerCustomer 启动器

echo.
echo ========================================
echo    AnswerCustomer 启动器
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.7或更高版本
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

:: 检查是否在项目目录
if not exist "run.py" (
    echo ❌ 请在AnswerCustomer项目目录中运行此脚本
    pause
    exit /b 1
)

:: 创建数据目录
if not exist "data" mkdir data
if not exist "data\csv" mkdir data\csv
if not exist "data\config" mkdir data\config

echo ✅ 数据目录检查完成

:: 安装依赖
echo.
echo 📦 正在安装项目依赖...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ✅ 依赖安装完成

:: 查找可用端口
echo.
echo 🔍 正在查找可用端口...
for /l %%i in (5000,1,5009) do (
    netstat -an | find "127.0.0.1:%%i" >nul 2>&1
    if errorlevel 1 (
        set PORT=%%i
        goto :found_port
    )
)
echo ❌ 无法找到可用端口
pause
exit /b 1

:found_port
echo ✅ 找到可用端口: %PORT%

:: 启动服务器
echo.
echo 🚀 正在启动服务器 (端口: %PORT%)...
echo.
echo ========================================
echo    服务器启动中，请稍候...
echo ========================================
echo.

:: 设置环境变量
set FLASK_APP=run.py
set FLASK_ENV=development

:: 启动服务器
start "" "http://localhost:%PORT%"
python run.py --port %PORT%

echo.
echo 🛑 服务器已停止
pause 
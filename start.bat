@echo off
chcp 65001 >nul
echo ============================================================
echo 🚀 AnswerCustomer 启动脚本 (Windows)
echo ============================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

REM 运行初始化脚本
echo 正在启动AnswerCustomer...
python init_and_run.py

if errorlevel 1 (
    echo.
    echo ❌ 启动失败，请检查错误信息
    pause
    exit /b 1
)

pause 
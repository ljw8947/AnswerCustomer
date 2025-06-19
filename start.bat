@echo off
chcp 65001 >nul
title AnswerCustomer Launcher

echo.
echo ========================================
echo    AnswerCustomer Launcher
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [31m Python not detected. Please install Python first.
    pause
    exit /b 1
)

:: Install dependencies
echo [34m Installing dependencies...
python -m pip install -r requirements.txt

:: Start server
echo [32m Starting server...
python run.py

pause 
@echo off
chcp 65001 >nul
title AnswerCustomer Launcher

echo.
echo ========================================
echo    AnswerCustomer Launcher
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [31m Python not detected. Please install Python 3.7 or higher.
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [32m Python environment check passed

:: Check if in project directory
if not exist "run.py" (
    echo [31m Please run this script in the AnswerCustomer project directory.
    pause
    exit /b 1
)

:: Create data directories
if not exist "data" mkdir data
if not exist "data\csv" mkdir data\csv
if not exist "data\config" mkdir data\config

echo [32m Data directory check complete

:: Install dependencies
echo.
echo [34m Installing project dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo [31m Dependency installation failed
    pause
    exit /b 1
)

echo [32m Dependencies installed successfully

:: Find available port
echo.
echo [33m Searching for available port...
for /l %%i in (5000,1,5009) do (
    netstat -an | find "127.0.0.1:%%i" >nul 2>&1
    if errorlevel 1 (
        set PORT=%%i
        goto :found_port
    )
)
echo [31m No available port found
pause
exit /b 1

:found_port
echo [32m Found available port: %PORT%

:: Start server
echo.
echo [32m Starting server (port: %PORT%)...
echo.
echo ========================================
echo    Server is starting, please wait...
echo ========================================
echo.

:: Set environment variables
set FLASK_APP=run.py
set FLASK_ENV=development

:: Start server
start "" "http://localhost:%PORT%"
python run.py --port %PORT%

echo.
echo [33m Server stopped
pause 
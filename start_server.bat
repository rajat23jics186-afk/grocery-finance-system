#!/bin/bash
# Windows batch script to start the Grocery Finance System

@echo off
title Grocery Finance System

echo.
echo ================================
echo Grocery Finance System Startup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install -q -r requirements.txt

REM Initialize database
echo.
echo Initializing database...
python init_db.py

REM Start the server
echo.
echo ================================
echo Starting FastAPI Server
echo ================================
echo API will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

python run.py

pause

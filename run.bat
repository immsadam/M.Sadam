@echo off
REM ============================================
REM AI Character Story Video Generator
REM Entry Point: BAT > Python > Ollama > ComfyUI
REM ============================================

echo.
echo ======== AI Character Story Video Generator ========
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if required folders exist
if not exist "input" mkdir input
if not exist "output" mkdir output
if not exist "logs" mkdir logs

echo Creating directories: input, output, logs
echo.

REM Install requirements if needed
echo Checking Python dependencies...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting main application...
echo.

REM Run main Python script
python main.py

pause

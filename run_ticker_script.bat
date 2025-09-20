@echo off
REM ================================
REM Stock Trading App - Run Script
REM ================================

REM Change directory to your project folder
cd /d %USERPROFILE%\Dev\stock-trading-python-app

REM Activate your virtual environment (uncomment if using venv)
%USERPROFILE%\Dev\stock-trading-python-app\venv\Scripts\activate.bat

REM Run the Python script
python script.py

REM Pause to see errors/output (optional - remove if scheduling)
REM pause

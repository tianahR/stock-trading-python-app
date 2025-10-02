@echo off
REM ================================
REM Stock Trading App - Run Script
REM ================================

REM Change directory to your project folder
cd /d %USERPROFILE%\Dev\stock-trading-python-app

REM Run Python script using the venv interpreter
%USERPROFILE%\Dev\stock-trading-python-app\.venv\Scripts\python.exe script.py

REM Pause so you can see errors when testing manually
REM pause

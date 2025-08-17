@echo off
REM ImagePathifier run script with venv

REM Create venv if not exists
if not exist venv (
    echo Virtual environment not found. Setting up...
    call setup_venv.bat
)

REM Activate and run
call venv\Scripts\activate && python ImagePathifier.py
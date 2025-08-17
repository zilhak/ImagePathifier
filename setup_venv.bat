@echo off
echo ========================================
echo   ImagePathifier Virtual Environment Setup
echo ========================================
echo.

REM Check Python version
py --version
echo.

REM Remove existing venv if exists
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

REM Create virtual environment
echo Creating virtual environment...
py -m venv venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install packages
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To run the program:
echo   1. venv\Scripts\activate
echo   2. python ImagePathifier.py
echo.
echo Or just run: run_with_venv.bat
echo ========================================
pause
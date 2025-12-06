@echo off
REM LUVORA Setup Script for Windows
REM This script sets up the development environment

echo ========================================
echo LUVORA E-commerce Platform Setup
echo ========================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/8] Checking Python version...
python --version

echo.
echo [2/8] Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists
) else (
    python -m venv .venv
    echo Virtual environment created
)

echo.
echo [3/8] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [4/8] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [5/8] Installing dependencies...
pip install -r requirements.txt

echo.
echo [6/8] Setting up environment file...
if exist .env (
    echo .env file already exists
) else (
    copy .env.example .env
    echo .env file created - Please update with your credentials
)

echo.
echo [7/8] Creating logs directory...
if not exist logs mkdir logs

echo.
echo [8/8] Running database migrations...
python manage.py migrate

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Update .env file with your database credentials
echo   2. Create a superuser: python manage.py createsuperuser
echo   3. Load sample data: python manage.py populate_sample_data
echo   4. Run server: python manage.py runserver
echo.
echo For detailed instructions, see QUICKSTART.md
echo.
pause

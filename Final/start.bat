@echo off
echo ========================================
echo    CampusLink - Student Utility Hub
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import flask, pymongo, flask_cors" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    python -m pip install flask flask-cors pymongo
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)

echo Dependencies OK!
echo.

REM Ask user if they want sample data
set /p choice="Do you want to populate sample data? (y/n): "
if /i "%choice%"=="y" (
    echo Populating sample data...
    python run.py --sample-data
) else (
    echo Starting application...
    python run.py
)

pause
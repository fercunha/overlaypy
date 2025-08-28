@echo off
REM Quick run script for OverlayPy on Windows

echo Starting OverlayPy...

REM Check if virtual environment exists
if not exist "localvenv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run the application
call localvenv\Scripts\activate.bat && python overlay.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    pause
)

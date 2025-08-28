@echo off
REM Windows Debug Script for OverlayPy
REM This script runs OverlayPy in debug mode and captures all output

setlocal enabledelayedexpansion

echo [INFO] Starting OverlayPy Windows Debug Session
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python and ensure it's in your PATH
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [INFO] Found !PYTHON_VERSION!

REM Check if virtual environment exists
if exist "localvenv" (
    echo [INFO] Activating virtual environment...
    call localvenv\Scripts\activate.bat
) else (
    echo [WARNING] No virtual environment found
    echo [INFO] Using system Python
)

REM Create debug output file
set TIMESTAMP=%date:~-4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set DEBUG_FILE=debug_%TIMESTAMP%.log

echo [INFO] Debug output will be saved to: %DEBUG_FILE%
echo [INFO] Real-time logs will also be shown in logs/ directory
echo.

REM Run in test mode first
echo [INFO] Running OverlayPy in TEST MODE (5 second test)...
echo --------------------------------------------------------
python overlay.py --test --debug > %DEBUG_FILE% 2>&1
set TEST_RESULT=!errorlevel!

echo.
if !TEST_RESULT! EQU 0 (
    echo [SUCCESS] Test mode completed successfully
) else (
    echo [ERROR] Test mode failed with exit code: !TEST_RESULT!
)

echo.
echo Test output:
echo ============
type %DEBUG_FILE%
echo ============
echo.

REM Ask if user wants to run interactive mode
choice /C YN /M "Do you want to run in interactive mode for manual testing? (Y/N)"
if errorlevel 2 goto :show_results

echo.
echo [INFO] Running OverlayPy in INTERACTIVE MODE...
echo -----------------------------------------------
echo Press Ctrl+C to exit when done testing
echo.
python overlay.py --debug

:show_results
echo.
echo [INFO] Debug session completed
echo.
echo Debug files created:
echo - %DEBUG_FILE% (this session)
if exist "logs" (
    echo - logs\overlaypy_*.log (detailed application logs)
    echo.
    echo Latest log files:
    dir /b /o-d logs\overlaypy_*.log | head -3
)

echo.
echo [INFO] System Information Summary:
echo ==================================
echo Platform: %OS%
echo Processor: %PROCESSOR_IDENTIFIER%
echo Python: !PYTHON_VERSION!
echo Working Directory: %CD%
echo.

echo [INFO] To share debug information:
echo 1. Copy the contents of %DEBUG_FILE%
echo 2. Include the latest log file from logs/ directory
echo 3. Mention your Windows version and Python version
echo.

pause

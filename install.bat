@echo off
REM OverlayPy Windows Installation Script
REM This script automates the setup process for OverlayPy on Windows

setlocal enabledelayedexpansion

echo [INFO] Starting OverlayPy installation for Windows...
echo ===================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [INFO] Found !PYTHON_VERSION!

REM Check Python version (should be 3.7+)
for /f "tokens=2 delims=. " %%i in ('python --version') do set PYTHON_MAJOR=%%i
for /f "tokens=3 delims=. " %%i in ('python --version') do set PYTHON_MINOR=%%i

if !PYTHON_MAJOR! LSS 3 (
    echo [ERROR] Python 3.7+ is required. Found Python !PYTHON_MAJOR!.!PYTHON_MINOR!
    pause
    exit /b 1
)

if !PYTHON_MAJOR! EQU 3 if !PYTHON_MINOR! LSS 7 (
    echo [ERROR] Python 3.7+ is required. Found Python !PYTHON_MAJOR!.!PYTHON_MINOR!
    pause
    exit /b 1
)

echo [SUCCESS] Python version is compatible

REM Check if virtual environment already exists
if exist "localvenv" (
    echo [INFO] Virtual environment already exists
    choice /C YN /M "Do you want to recreate it? (Y/N)"
    if errorlevel 2 goto :skip_venv_creation
    echo [INFO] Removing existing virtual environment...
    rmdir /s /q localvenv
)

REM Create virtual environment
echo [INFO] Creating virtual environment...
python -m venv localvenv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

:skip_venv_creation

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call localvenv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Ask if user wants to install build dependencies
echo.
choice /C YN /M "Do you want to install build dependencies for creating executables? (Y/N)"
if errorlevel 2 goto :skip_build_deps

echo [INFO] Installing build dependencies...
pip install pyinstaller>=6.0.0
if errorlevel 1 (
    echo [WARNING] Failed to install PyInstaller
) else (
    echo [SUCCESS] PyInstaller installed successfully
)

pip install pillow>=10.0.0
if errorlevel 1 (
    echo [WARNING] Failed to install Pillow (icon support)
) else (
    echo [SUCCESS] Pillow installed successfully
)

pip install wheel setuptools
if errorlevel 1 (
    echo [WARNING] Failed to install build tools
) else (
    echo [SUCCESS] Build tools installed successfully
)

echo [INFO] Build dependencies installation completed
echo You can now use build-windows.bat to create executables
echo.

:skip_build_deps

REM Test installation
echo [INFO] Testing installation...
python -c "import tkinter; import screeninfo; print('All dependencies installed successfully')"
if errorlevel 1 (
    echo [ERROR] Installation test failed
    pause
    exit /b 1
)

echo [SUCCESS] Installation completed successfully!
echo.
echo To run OverlayPy:
echo   1. Open Command Prompt in this directory
echo   2. Run: localvenv\Scripts\activate.bat
echo   3. Run: python overlay.py
echo.
echo Or simply double-click on run-overlay.bat
echo.
pause

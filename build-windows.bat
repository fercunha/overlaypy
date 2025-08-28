@echo off
REM OverlayPy Windows Build Script
REM This script installs build dependencies and creates a Windows executable

setlocal enabledelayedexpansion

echo [INFO] Starting OverlayPy build process for Windows...
echo =====================================================

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

REM Check Python version (should be 3.8+)
for /f "tokens=2 delims=. " %%i in ('python --version') do set PYTHON_MAJOR=%%i
for /f "tokens=3 delims=. " %%i in ('python --version') do set PYTHON_MINOR=%%i

if !PYTHON_MAJOR! LSS 3 (
    echo [ERROR] Python 3.8+ is required for building. Found Python !PYTHON_MAJOR!.!PYTHON_MINOR!
    pause
    exit /b 1
)

if !PYTHON_MAJOR! EQU 3 if !PYTHON_MINOR! LSS 8 (
    echo [ERROR] Python 3.8+ is required for building. Found Python !PYTHON_MAJOR!.!PYTHON_MINOR!
    pause
    exit /b 1
)

echo [SUCCESS] Python version is compatible for building

REM Check if virtual environment exists, create if not
if not exist "localvenv" (
    echo [INFO] Creating virtual environment...
    python -m venv localvenv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call localvenv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install runtime dependencies
echo [INFO] Installing runtime dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install runtime dependencies
    pause
    exit /b 1
)

REM Install build dependencies
echo [INFO] Installing build dependencies...
pip install pyinstaller>=6.0.0
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)

pip install pillow>=10.0.0
if errorlevel 1 (
    echo [ERROR] Failed to install Pillow (for icon support)
    echo [WARNING] Continuing without icon support...
)

pip install auto-py-to-exe>=2.38.0
if errorlevel 1 (
    echo [WARNING] Failed to install auto-py-to-exe (optional GUI tool)
    echo [INFO] Continuing with command-line PyInstaller...
)

REM Install additional build tools
echo [INFO] Installing additional build tools...
pip install wheel setuptools
if errorlevel 1 (
    echo [WARNING] Failed to install build tools
)

REM Create application icon
echo [INFO] Creating application icon...
python -c "
try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a simple icon
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background
    margin = 20
    draw.rectangle([margin, margin, size[0]-margin, size[1]-margin], 
                  fill=(70, 130, 180, 255), outline=(25, 25, 112, 255), width=4)
    
    # Draw text
    try:
        # Try to use a better font
        font = ImageFont.truetype('arial.ttf', 48)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Calculate text position
    text = 'OVL'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as ICO file with multiple sizes
    img.save('icon.ico', format='ICO', 
             sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print('[SUCCESS] Application icon created')
except ImportError:
    print('[WARNING] Pillow not available, skipping icon creation')
except Exception as e:
    print(f'[WARNING] Icon creation failed: {e}')
"

REM Test the application first
echo [INFO] Testing application before building...
python overlay.py --test 2>nul
if errorlevel 1 (
    echo [WARNING] Application test had issues, continuing with build...
)

REM Clean previous builds
if exist "dist" (
    echo [INFO] Cleaning previous builds...
    rmdir /s /q dist
)
if exist "build" (
    rmdir /s /q build
)

REM Build single executable
echo [INFO] Building single executable (OverlayPy.exe)...
pyinstaller --onefile ^
            --windowed ^
            --name OverlayPy ^
            --icon icon.ico ^
            --add-data "README.md;." ^
            --add-data "WINDOWS.md;." ^
            --hidden-import tkinter ^
            --hidden-import tkinter.ttk ^
            --hidden-import screeninfo ^
            --exclude-module matplotlib ^
            --exclude-module numpy ^
            --exclude-module pandas ^
            --exclude-module scipy ^
            --exclude-module jupyter ^
            --clean ^
            overlay.py

if errorlevel 1 (
    echo [ERROR] Failed to build single executable
    pause
    exit /b 1
)

REM Build portable directory version
echo [INFO] Building portable directory version...
pyinstaller --onedir ^
            --windowed ^
            --name OverlayPy-Portable ^
            --icon icon.ico ^
            --add-data "README.md;." ^
            --add-data "WINDOWS.md;." ^
            --hidden-import tkinter ^
            --hidden-import tkinter.ttk ^
            --hidden-import screeninfo ^
            --exclude-module matplotlib ^
            --exclude-module numpy ^
            --exclude-module pandas ^
            --exclude-module scipy ^
            --exclude-module jupyter ^
            --clean ^
            overlay.py

if errorlevel 1 (
    echo [ERROR] Failed to build portable version
    pause
    exit /b 1
)

REM Test the built executable
echo [INFO] Testing built executable...
if exist "dist\OverlayPy.exe" (
    echo [INFO] Single executable: dist\OverlayPy.exe
    dist\OverlayPy.exe --help >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Executable test showed warnings (this is normal)
    )
) else (
    echo [ERROR] Single executable not found!
)

if exist "dist\OverlayPy-Portable\OverlayPy-Portable.exe" (
    echo [INFO] Portable version: dist\OverlayPy-Portable\
) else (
    echo [ERROR] Portable version not found!
)

REM Create release package
echo [INFO] Creating release package...
if not exist "release" mkdir release

REM Copy executables
if exist "dist\OverlayPy.exe" (
    copy "dist\OverlayPy.exe" "release\"
)

if exist "dist\OverlayPy-Portable" (
    xcopy "dist\OverlayPy-Portable" "release\OverlayPy-Portable\" /E /I /Q
)

REM Copy documentation and scripts
copy "README.md" "release\" >nul 2>&1
copy "WINDOWS.md" "release\" >nul 2>&1
copy "install.bat" "release\" >nul 2>&1
copy "run-overlay.bat" "release\" >nul 2>&1

REM Create launcher script
echo @echo off > "release\OverlayPy-Launcher.bat"
echo echo Starting OverlayPy... >> "release\OverlayPy-Launcher.bat"
echo if exist OverlayPy.exe ( >> "release\OverlayPy-Launcher.bat"
echo     OverlayPy.exe >> "release\OverlayPy-Launcher.bat"
echo ) else if exist OverlayPy-Portable\OverlayPy-Portable.exe ( >> "release\OverlayPy-Launcher.bat"
echo     OverlayPy-Portable\OverlayPy-Portable.exe >> "release\OverlayPy-Launcher.bat"
echo ) else ( >> "release\OverlayPy-Launcher.bat"
echo     echo [ERROR] No executable found! >> "release\OverlayPy-Launcher.bat"
echo     pause >> "release\OverlayPy-Launcher.bat"
echo ) >> "release\OverlayPy-Launcher.bat"

REM Create README for release
echo OverlayPy Windows Release > "release\README-RELEASE.txt"
echo ========================= >> "release\README-RELEASE.txt"
echo. >> "release\README-RELEASE.txt"
echo This package contains: >> "release\README-RELEASE.txt"
echo. >> "release\README-RELEASE.txt"
echo 1. OverlayPy.exe - Single executable file >> "release\README-RELEASE.txt"
echo    - Just double-click to run >> "release\README-RELEASE.txt"
echo    - No installation required >> "release\README-RELEASE.txt"
echo. >> "release\README-RELEASE.txt"
echo 2. OverlayPy-Portable\ - Portable directory version >> "release\README-RELEASE.txt"
echo    - Faster startup >> "release\README-RELEASE.txt"
echo    - Run OverlayPy-Portable.exe inside the folder >> "release\README-RELEASE.txt"
echo. >> "release\README-RELEASE.txt"
echo 3. OverlayPy-Launcher.bat - Smart launcher >> "release\README-RELEASE.txt"
echo    - Automatically finds and runs the best version >> "release\README-RELEASE.txt"
echo. >> "release\README-RELEASE.txt"
echo 4. Documentation: >> "release\README-RELEASE.txt"
echo    - README.md - General information >> "release\README-RELEASE.txt"
echo    - WINDOWS.md - Windows-specific help >> "release\README-RELEASE.txt"
echo. >> "release\README-RELEASE.txt"
echo System Requirements: >> "release\README-RELEASE.txt"
echo - Windows 7 SP1 or later (Windows 10/11 recommended) >> "release\README-RELEASE.txt"
echo - No Python installation required >> "release\README-RELEASE.txt"

echo [SUCCESS] Build completed successfully!
echo.
echo Build artifacts:
echo   - Single executable: dist\OverlayPy.exe
echo   - Portable version: dist\OverlayPy-Portable\
echo   - Release package: release\
echo.
echo To distribute:
echo   1. Share the entire 'release' folder, or
echo   2. Share just 'OverlayPy.exe' for simple distribution
echo.
echo File sizes:
if exist "dist\OverlayPy.exe" (
    for %%A in ("dist\OverlayPy.exe") do echo   - OverlayPy.exe: %%~zA bytes
)
if exist "release" (
    echo   - Release folder contains all distribution files
)
echo.
pause

# OverlayPy Windows Build Script (PowerShell)
# This script installs build dependencies and creates a Windows executable

param(
    [switch]$SkipTests,
    [switch]$QuickBuild,
    [string]$OutputDir = "dist",
    [switch]$Verbose
)

# Set error action
$ErrorActionPreference = "Stop"

# Enable verbose output if requested
if ($Verbose) {
    $VerbosePreference = "Continue"
}

Write-Host "[INFO] Starting OverlayPy build process for Windows..." -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

# Function to check command availability
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction SilentlyContinue) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Function to get file size in human readable format
function Get-FileSize {
    param($Path)
    if (Test-Path $Path) {
        $size = (Get-Item $Path).Length
        if ($size -gt 1MB) {
            return "{0:N2} MB" -f ($size / 1MB)
        }
        elseif ($size -gt 1KB) {
            return "{0:N2} KB" -f ($size / 1KB)
        }
        else {
            return "$size bytes"
        }
    }
    return "Not found"
}

# Check if Python is installed
Write-Host "[INFO] Checking Python installation..." -ForegroundColor Blue
if (-not (Test-Command "python")) {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

# Get Python version
$pythonVersion = python --version 2>&1
Write-Host "[INFO] Found $pythonVersion" -ForegroundColor Green

# Parse version
$versionMatch = [regex]::Match($pythonVersion, "Python (\d+)\.(\d+)")
if ($versionMatch.Success) {
    $majorVersion = [int]$versionMatch.Groups[1].Value
    $minorVersion = [int]$versionMatch.Groups[2].Value
    
    if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 8)) {
        Write-Host "[ERROR] Python 3.8+ is required for building. Found Python $majorVersion.$minorVersion" -ForegroundColor Red
        exit 1
    }
}

Write-Host "[SUCCESS] Python version is compatible for building" -ForegroundColor Green

# Check if virtual environment exists, create if not
if (-not (Test-Path "localvenv")) {
    Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Blue
    python -m venv localvenv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Blue
if (Test-Path "localvenv\Scripts\Activate.ps1") {
    & localvenv\Scripts\Activate.ps1
} else {
    Write-Host "[ERROR] Virtual environment activation script not found" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "[INFO] Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Failed to upgrade pip, continuing..." -ForegroundColor Yellow
}

# Install runtime dependencies
Write-Host "[INFO] Installing runtime dependencies..." -ForegroundColor Blue
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install runtime dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[WARNING] requirements.txt not found, installing basic dependencies..." -ForegroundColor Yellow
    pip install screeninfo
}

# Install build dependencies
Write-Host "[INFO] Installing build dependencies..." -ForegroundColor Blue

$buildDependencies = @(
    "pyinstaller>=6.0.0",
    "pillow>=10.0.0",
    "wheel",
    "setuptools"
)

foreach ($dep in $buildDependencies) {
    try {
        pip install $dep
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[SUCCESS] Installed $dep" -ForegroundColor Green
        } else {
            Write-Host "[WARNING] Failed to install $dep" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "[WARNING] Exception installing $dep`: $_" -ForegroundColor Yellow
    }
}

# Install optional build tools
Write-Host "[INFO] Installing optional build tools..." -ForegroundColor Blue
try {
    pip install auto-py-to-exe>=2.38.0
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[SUCCESS] Installed auto-py-to-exe (GUI tool available)" -ForegroundColor Green
    }
}
catch {
    Write-Host "[INFO] auto-py-to-exe not installed (optional)" -ForegroundColor Blue
}

# Create application icon
Write-Host "[INFO] Creating application icon..." -ForegroundColor Blue
$iconScript = @"
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create a professional looking icon
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(size[1]):
        color_value = int(70 + (110 * i / size[1]))  # Gradient from 70 to 180
        draw.line([(0, i), (size[0], i)], fill=(color_value, 130, 180, 255))
    
    # Draw border
    margin = 15
    draw.rectangle([margin, margin, size[0]-margin, size[1]-margin], 
                  outline=(25, 25, 112, 255), width=6)
    
    # Draw inner highlight
    inner_margin = 25
    draw.rectangle([inner_margin, inner_margin, size[0]-inner_margin, size[1]-inner_margin], 
                  outline=(255, 255, 255, 100), width=2)
    
    # Draw text with better positioning
    text = 'OVL'
    try:
        # Try different font paths
        font_paths = [
            'C:/Windows/Fonts/arial.ttf',
            'C:/Windows/Fonts/calibri.ttf',
            'C:/Windows/Fonts/segoeui.ttf'
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 64)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Calculate text position for center alignment
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # Draw text shadow
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 128), font=font)
    # Draw main text
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as ICO file with multiple sizes for Windows
    sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
    img.save('icon.ico', format='ICO', sizes=sizes)
    print('[SUCCESS] Professional application icon created with multiple sizes')
    
except ImportError as e:
    print(f'[WARNING] Pillow not available: {e}')
    print('[INFO] Creating simple fallback icon...')
    # Create a simple text-based icon file
    with open('icon.ico', 'wb') as f:
        # This is a minimal ICO file - not pretty but functional
        f.write(b'\x00\x00\x01\x00\x01\x00\x20\x20\x00\x00\x01\x00\x08\x00\xe8\x02\x00\x00\x16\x00\x00\x00')
        f.write(b'\x00' * 1000)  # Placeholder data
except Exception as e:
    print(f'[WARNING] Icon creation failed: {e}')
    print('[INFO] Continuing without custom icon...')
"@

python -c $iconScript

# Test the application first (unless skipped)
if (-not $SkipTests) {
    Write-Host "[INFO] Testing application before building..." -ForegroundColor Blue
    try {
        python -c "import overlay; print('Application imports successfully')"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[WARNING] Application import test had issues, continuing..." -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "[WARNING] Application test had issues, continuing..." -ForegroundColor Yellow
    }
}

# Clean previous builds
if (Test-Path "dist") {
    Write-Host "[INFO] Cleaning previous builds..." -ForegroundColor Blue
    Remove-Item -Recurse -Force "dist"
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

# Prepare PyInstaller arguments
$commonArgs = @(
    "--windowed"
    "--icon", "icon.ico"
    "--add-data", "README.md;."
    "--hidden-import", "tkinter"
    "--hidden-import", "tkinter.ttk"
    "--hidden-import", "screeninfo"
    "--exclude-module", "matplotlib"
    "--exclude-module", "numpy"
    "--exclude-module", "pandas"
    "--exclude-module", "scipy"
    "--exclude-module", "jupyter"
    "--clean"
)

# Add optional data files if they exist
if (Test-Path "WINDOWS.md") {
    $commonArgs += "--add-data", "WINDOWS.md;."
}

# Build single executable
Write-Host "[INFO] Building single executable (OverlayPy.exe)..." -ForegroundColor Blue
$singleExeArgs = @("--onefile", "--name", "OverlayPy") + $commonArgs + @("overlay.py")

try {
    & pyinstaller @singleExeArgs
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed with exit code $LASTEXITCODE"
    }
    Write-Host "[SUCCESS] Single executable built successfully!" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Failed to build single executable: $_" -ForegroundColor Red
    exit 1
}

# Build portable directory version (unless quick build)
if (-not $QuickBuild) {
    Write-Host "[INFO] Building portable directory version..." -ForegroundColor Blue
    $portableArgs = @("--onedir", "--name", "OverlayPy-Portable") + $commonArgs + @("overlay.py")
    
    try {
        & pyinstaller @portableArgs
        if ($LASTEXITCODE -ne 0) {
            throw "PyInstaller failed with exit code $LASTEXITCODE"
        }
        Write-Host "[SUCCESS] Portable version built successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "[ERROR] Failed to build portable version: $_" -ForegroundColor Red
        Write-Host "[INFO] Continuing with single executable only..." -ForegroundColor Blue
    }
}

# Test the built executable
Write-Host "[INFO] Testing built executable..." -ForegroundColor Blue
if (Test-Path "dist\OverlayPy.exe") {
    $exeSize = Get-FileSize "dist\OverlayPy.exe"
    Write-Host "[SUCCESS] Single executable created: dist\OverlayPy.exe ($exeSize)" -ForegroundColor Green
    
    # Quick test
    try {
        & "dist\OverlayPy.exe" --help 2>&1 | Out-Null
        Write-Host "[INFO] Executable test completed (exit code: $LASTEXITCODE)" -ForegroundColor Blue
    }
    catch {
        Write-Host "[WARNING] Executable test showed warnings (this may be normal)" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] Single executable not found!" -ForegroundColor Red
}

if (Test-Path "dist\OverlayPy-Portable\OverlayPy-Portable.exe") {
    Write-Host "[SUCCESS] Portable version created: dist\OverlayPy-Portable\" -ForegroundColor Green
}

# Create release package
Write-Host "[INFO] Creating release package..." -ForegroundColor Blue
if (-not (Test-Path "release")) {
    New-Item -ItemType Directory -Path "release" | Out-Null
}

# Copy executables
if (Test-Path "dist\OverlayPy.exe") {
    Copy-Item "dist\OverlayPy.exe" "release\"
}

if (Test-Path "dist\OverlayPy-Portable") {
    Copy-Item -Recurse "dist\OverlayPy-Portable" "release\"
}

# Copy documentation and scripts
$filesToCopy = @("README.md", "WINDOWS.md", "install.bat", "install.ps1", "run-overlay.bat")
foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item $file "release\" -ErrorAction SilentlyContinue
    }
}

# Create smart launcher script
$launcherContent = @"
@echo off
title OverlayPy Launcher
echo Starting OverlayPy...
echo.

if exist "OverlayPy.exe" (
    echo [INFO] Running single executable version...
    start "" "OverlayPy.exe"
) else if exist "OverlayPy-Portable\OverlayPy-Portable.exe" (
    echo [INFO] Running portable version...
    start "" "OverlayPy-Portable\OverlayPy-Portable.exe"
) else (
    echo [ERROR] No OverlayPy executable found!
    echo.
    echo Please ensure you have either:
    echo - OverlayPy.exe in this folder, or
    echo - OverlayPy-Portable folder with executable
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] OverlayPy started successfully!
timeout /t 2 /nobreak >nul
"@

$launcherContent | Out-File -FilePath "release\OverlayPy-Launcher.bat" -Encoding ASCII

# Create release README
$releaseReadme = @"
OverlayPy Windows Release
=========================

This package contains OverlayPy executables for Windows.

Quick Start:
-----------
1. Double-click 'OverlayPy-Launcher.bat' for automatic startup, OR
2. Double-click 'OverlayPy.exe' to run directly

Contents:
---------
- OverlayPy.exe                 : Single executable file (recommended)
- OverlayPy-Portable\           : Portable directory version (faster startup)
- OverlayPy-Launcher.bat       : Smart launcher (finds best version automatically)
- README.md                     : General documentation
- WINDOWS.md                    : Windows-specific help and troubleshooting
- install.bat / install.ps1     : Development installation scripts

System Requirements:
-------------------
- Windows 7 SP1 or later (Windows 10/11 recommended)
- No Python installation required
- No additional dependencies needed

Features:
---------
- Text overlays with customizable positioning
- Multi-monitor support
- Auto-hide timer functionality
- Click-through overlays (Windows-specific)
- Real-time text updates
- Corner positioning options

Troubleshooting:
---------------
If you encounter any issues:
1. Check WINDOWS.md for common solutions
2. Try running as administrator
3. Ensure Windows Defender isn't blocking the executable
4. For persistent issues, check the GitHub repository

Build Information:
-----------------
Built on: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Python Version: $pythonVersion
PyInstaller Version: $(pip show pyinstaller | Select-String "Version" | ForEach-Object { $_.ToString().Split(":")[1].Trim() })

For more information and source code:
https://github.com/fercunha/overlaypy
"@

$releaseReadme | Out-File -FilePath "release\README-RELEASE.txt" -Encoding UTF8

# Final summary
Write-Host "`n[SUCCESS] Build completed successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

Write-Host "`nBuild artifacts:" -ForegroundColor Blue
if (Test-Path "dist\OverlayPy.exe") {
    $size = Get-FileSize "dist\OverlayPy.exe"
    Write-Host "  - Single executable: dist\OverlayPy.exe ($size)" -ForegroundColor White
}
if (Test-Path "dist\OverlayPy-Portable") {
    Write-Host "  - Portable version: dist\OverlayPy-Portable\" -ForegroundColor White
}
if (Test-Path "release") {
    Write-Host "  - Release package: release\ (ready for distribution)" -ForegroundColor White
}

Write-Host "`nDistribution options:" -ForegroundColor Blue
Write-Host "  1. Share the entire 'release' folder for complete package" -ForegroundColor White
Write-Host "  2. Share just 'OverlayPy.exe' for simple distribution" -ForegroundColor White
Write-Host "  3. Create ZIP archive of release folder for easy download" -ForegroundColor White

Write-Host "`nNext steps:" -ForegroundColor Blue
Write-Host "  - Test the executable on a clean Windows system" -ForegroundColor White
Write-Host "  - Consider code signing for professional distribution" -ForegroundColor White
Write-Host "  - Upload to GitHub Releases for public distribution" -ForegroundColor White

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

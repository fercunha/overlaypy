# OverlayPy PowerShell Installation Script
# Advanced Windows installation with better error handling

param(
    [switch]$Clean,
    [switch]$Verbose,
    [switch]$Help
)

# Color functions
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    switch ($Color) {
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Blue" { Write-Host $Message -ForegroundColor Blue }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        default { Write-Host $Message }
    }
}

function Write-Info { param([string]$Message) Write-ColorOutput "[INFO] $Message" "Blue" }
function Write-Success { param([string]$Message) Write-ColorOutput "[SUCCESS] $Message" "Green" }
function Write-Warning { param([string]$Message) Write-ColorOutput "[WARNING] $Message" "Yellow" }
function Write-Error { param([string]$Message) Write-ColorOutput "[ERROR] $Message" "Red" }

if ($Help) {
    Write-Host @"
OverlayPy PowerShell Installation Script

USAGE:
    .\install.ps1 [OPTIONS]

OPTIONS:
    -Clean      Remove existing virtual environment before creating new one
    -Verbose    Enable verbose output
    -Help       Show this help message

EXAMPLES:
    .\install.ps1                    # Normal installation
    .\install.ps1 -Clean            # Clean installation
    .\install.ps1 -Verbose          # Verbose installation
"@
    exit 0
}

Write-Info "Starting OverlayPy installation for Windows (PowerShell)"
Write-Host "================================================================"

# Check execution policy
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Warning "PowerShell execution policy is Restricted"
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
}

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Success "Found $pythonVersion"
} catch {
    Write-Error "Python is not installed or not in PATH"
    Write-Host "Please install Python from https://python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Read-Host "Press Enter to exit"
    exit 1
}

# Validate Python version
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $majorVersion = [int]$matches[1]
    $minorVersion = [int]$matches[2]
    
    if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 7)) {
        Write-Error "Python 3.7+ is required. Found Python $majorVersion.$minorVersion"
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Success "Python version is compatible"
} else {
    Write-Warning "Could not parse Python version"
}

# Handle existing virtual environment
if (Test-Path "localvenv") {
    if ($Clean) {
        Write-Info "Removing existing virtual environment..."
        Remove-Item -Recurse -Force "localvenv"
    } else {
        Write-Info "Virtual environment already exists"
        $choice = Read-Host "Do you want to recreate it? (y/N)"
        if ($choice -eq "y" -or $choice -eq "Y") {
            Write-Info "Removing existing virtual environment..."
            Remove-Item -Recurse -Force "localvenv"
        } else {
            Write-Info "Using existing virtual environment"
            $skipVenvCreation = $true
        }
    }
}

# Create virtual environment
if (-not $skipVenvCreation) {
    Write-Info "Creating virtual environment..."
    & python -m venv localvenv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment and install dependencies
Write-Info "Activating virtual environment and installing dependencies..."
& "localvenv\Scripts\python.exe" -m pip install --upgrade pip

if (Test-Path "requirements.txt") {
    & "localvenv\Scripts\pip.exe" install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install dependencies"
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Warning "requirements.txt not found, installing basic dependencies..."
    & "localvenv\Scripts\pip.exe" install screeninfo Cython pyobjc-core pyobjc-framework-Cocoa
}

# Test installation
Write-Info "Testing installation..."
$testResult = & "localvenv\Scripts\python.exe" -c "import tkinter; import screeninfo; print('SUCCESS: All dependencies installed')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Installation test failed: $testResult"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Success "Installation completed successfully!"
Write-Host ""
Write-Host "To run OverlayPy:" -ForegroundColor Cyan
Write-Host "  Method 1: Double-click 'run-overlay.bat'" -ForegroundColor White
Write-Host "  Method 2: Run the following commands:" -ForegroundColor White
Write-Host "    localvenv\Scripts\activate" -ForegroundColor Gray
Write-Host "    python overlay.py" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"

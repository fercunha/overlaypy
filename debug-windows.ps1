# Windows Debug Script for OverlayPy (PowerShell)
# This script runs OverlayPy in debug mode and captures detailed information

param(
    [switch]$TestOnly,
    [switch]$InteractiveOnly,
    [switch]$Verbose
)

# Function to write colored output
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Blue }
function Write-Success { param($Message) Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

Write-Host "OverlayPy Windows Debug Session" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Info "Checking Python installation..."
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Found $pythonVersion"
    } else {
        throw "Python not found"
    }
} catch {
    Write-Error "Python is not installed or not in PATH"
    Write-Host "Please install Python from https://python.org/downloads/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check virtual environment
if (Test-Path "localvenv") {
    Write-Info "Activating virtual environment..."
    try {
        & "localvenv\Scripts\Activate.ps1"
        Write-Success "Virtual environment activated"
    } catch {
        Write-Warning "Failed to activate virtual environment, using system Python"
    }
} else {
    Write-Warning "No virtual environment found, using system Python"
}

# Collect system information
Write-Info "Collecting system information..."
$systemInfo = @{
    "OS" = (Get-WmiObject Win32_OperatingSystem).Caption
    "Version" = (Get-WmiObject Win32_OperatingSystem).Version
    "Architecture" = (Get-WmiObject Win32_OperatingSystem).OSArchitecture
    "Python" = $pythonVersion
    "PowerShell" = $PSVersionTable.PSVersion.ToString()
    "Processor" = (Get-WmiObject Win32_Processor).Name
    "Memory" = "{0:N2} GB" -f ((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
    "WorkingDir" = $PWD.Path
    "Timestamp" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

Write-Host ""
Write-Host "System Information:" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
foreach ($key in $systemInfo.Keys) {
    Write-Host "  $key`: $($systemInfo[$key])" -ForegroundColor White
}

# Create debug output file
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$debugFile = "debug_$timestamp.log"

Write-Host ""
Write-Info "Debug output will be saved to: $debugFile"
Write-Info "Real-time logs will also be shown in logs/ directory"

# Function to invoke Python with logging
function Invoke-OverlayPy {
    param($Arguments, $Description)
    
    Write-Host ""
    Write-Info $Description
    Write-Host ("-" * $Description.Length) -ForegroundColor Gray
    
    $startTime = Get-Date
    
    try {
        # Run Python and capture all output
        $output = & python overlay.py @Arguments 2>&1
        $exitCode = $LASTEXITCODE
        
        $endTime = Get-Date
        $duration = $endTime - $startTime
        
        # Save output to debug file
        $logEntry = @"
========================================
$Description
Started: $startTime
Ended: $endTime
Duration: $($duration.TotalSeconds) seconds
Exit Code: $exitCode
========================================
$output
========================================

"@
        Add-Content -Path $debugFile -Value $logEntry
        
        # Display result
        if ($exitCode -eq 0) {
            Write-Success "$Description completed successfully in $($duration.TotalSeconds) seconds"
        } else {
            Write-Error "$Description failed with exit code: $exitCode"
        }
        
        # Show output if verbose or if there was an error
        if ($Verbose -or $exitCode -ne 0) {
            Write-Host ""
            Write-Host "Output:" -ForegroundColor Gray
            Write-Host "-------" -ForegroundColor Gray
            $output | ForEach-Object { Write-Host $_ -ForegroundColor Gray }
        }
        
        return $exitCode
    }
    catch {
        Write-Error "Failed to run Python: $_"
        return 1
    }
}

# Save system info to debug file
$systemInfo.GetEnumerator() | Sort-Object Key | ForEach-Object {
    "$($_.Key): $($_.Value)"
} | Out-File -FilePath $debugFile -Encoding UTF8

# Run tests based on parameters
if (-not $InteractiveOnly) {
    # Test mode
    $testResult = Invoke-OverlayPy @("--test", "--debug") "Running OverlayPy in TEST MODE (3 second test)"
    
    if ($testResult -eq 0) {
        Write-Success "Basic functionality test passed!"
    } else {
        Write-Error "Basic functionality test failed!"
    }
}

if (-not $TestOnly) {
    # Ask about interactive mode
    Write-Host ""
    $runInteractive = Read-Host "Do you want to run in interactive mode for manual testing? (y/N)"
    
    if ($runInteractive -match "^[Yy]") {
        Write-Host ""
        Write-Info "Running OverlayPy in INTERACTIVE MODE..."
        Write-Host "Press Ctrl+C to exit when done testing" -ForegroundColor Yellow
        Write-Host ""
        
        try {
            & python overlay.py --debug
        }
        catch {
            Write-Warning "Interactive mode interrupted"
        }
    }
}

# Show results
Write-Host ""
Write-Host "Debug Session Results" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan

Write-Info "Debug files created:"
Write-Host "  - $debugFile (this session)" -ForegroundColor White

if (Test-Path "logs") {
    $logFiles = Get-ChildItem "logs\overlaypy_*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 3
    if ($logFiles) {
        Write-Host "  - logs\overlaypy_*.log (detailed application logs)" -ForegroundColor White
        Write-Host ""
        Write-Info "Latest log files:"
        foreach ($file in $logFiles) {
            $size = "{0:N2} KB" -f ($file.Length / 1KB)
            Write-Host "    $($file.Name) ($size, $($file.LastWriteTime))" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Info "To share debug information:"
Write-Host "  1. Copy the contents of $debugFile" -ForegroundColor White
Write-Host "  2. Include the latest log file from logs/ directory" -ForegroundColor White
Write-Host "  3. Mention your Windows version and Python version" -ForegroundColor White

# Check for common issues
Write-Host ""
Write-Info "Checking for common issues..."

$issues = @()

# Check screen resolution
try {
    $screen = Get-WmiObject Win32_VideoController | Where-Object { $_.Name -notlike "*Remote*" } | Select-Object -First 1
    if ($screen) {
        Write-Success "Display adapter: $($screen.Name)"
    } else {
        $issues += "Could not detect display adapter"
    }
} catch {
    $issues += "Failed to check display information"
}

# Check for multiple monitors
try {
    $monitors = Get-WmiObject WmiMonitorID -Namespace root\wmi
    if ($monitors) {
        Write-Success "Detected $($monitors.Count) monitor(s)"
    } else {
        $issues += "Could not detect monitors"
    }
} catch {
    $issues += "Failed to check monitor information"
}

# Check Windows version compatibility
$winVersion = [System.Environment]::OSVersion.Version
if ($winVersion.Major -lt 10) {
    $issues += "Windows version might not support all features (Windows 10+ recommended)"
}

if ($issues) {
    Write-Host ""
    Write-Warning "Potential issues detected:"
    foreach ($issue in $issues) {
        Write-Host "  - $issue" -ForegroundColor Yellow
    }
}

Write-Host ""
Read-Host "Press Enter to exit"

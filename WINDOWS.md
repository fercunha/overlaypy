# Windows Troubleshooting Guide for OverlayPy

## Common Issues and Solutions

### 1. Python Not Found
**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
- Install Python from https://python.org/downloads/
- **Important:** Check "Add Python to PATH" during installation
- If already installed, manually add Python to PATH:
  1. Find Python installation (usually `C:\Users\{username}\AppData\Local\Programs\Python\Python{version}\`)
  2. Add to System PATH environment variable

### 2. Tkinter Import Error
**Error:** `ModuleNotFoundError: No module named 'tkinter'`

**Solution:**
- Tkinter should come with Python by default on Windows
- If missing, reinstall Python with "tcl/tk and IDLE" option checked
- Or install via: `pip install tk`

### 3. Virtual Environment Creation Failed
**Error:** `Error: Microsoft Visual C++ 14.0 is required`

**Solution:**
- Install Microsoft C++ Build Tools
- Or install Visual Studio Community with C++ development tools
- Alternative: Use `python -m venv --system-site-packages localvenv`

### 4. Permission Errors
**Error:** `PermissionError: [WinError 5] Access is denied`

**Solution:**
- Run Command Prompt as Administrator
- Or install in user directory instead of system-wide
- Check antivirus software isn't blocking the installation

### 5. PowerShell Execution Policy
**Error:** `execution of scripts is disabled on this system`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 6. Click-through Feature Not Working
**Error:** Click-through functionality fails silently

**Solution:**
- This is normal behavior - the overlay will still work
- Click-through requires administrator privileges on some Windows versions
- Feature may not work in Windows Safe Mode

### 7. Overlay Not Visible
**Issue:** Overlay window doesn't appear

**Solutions:**
- Check if overlay is behind other windows
- Try different corner positions
- Restart the application
- Check Windows display scaling settings
- Ensure multiple monitors are detected correctly

### 8. High DPI Display Issues
**Issue:** Text appears too small or large on high DPI displays

**Solutions:**
- Adjust font size in the application
- Change Windows display scaling settings
- Use Windows compatibility mode

## Installation Methods

### Method 1: Batch Script (Recommended)
```cmd
install.bat
```

### Method 2: PowerShell Script
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Method 3: Manual Installation
```cmd
python -m venv localvenv
localvenv\Scripts\activate
pip install -r requirements.txt
python overlay.py
```

## Running the Application

### Quick Start
- Double-click `run-overlay.bat`

### Manual Start
```cmd
localvenv\Scripts\activate
python overlay.py
```

### From PowerShell
```powershell
.\localvenv\Scripts\Activate.ps1
python overlay.py
```

## System Requirements

- **OS:** Windows 7 SP1 or later (Windows 10/11 recommended)
- **Python:** 3.7+ (3.9+ recommended)
- **RAM:** 100MB free
- **Disk:** 50MB free space
- **Display:** Any resolution (multi-monitor supported)

## Performance Tips

1. **Close unnecessary applications** to reduce system load
2. **Use smaller font sizes** for better performance
3. **Minimize padding** to reduce overlay window size
4. **Disable antivirus real-time scanning** for the OverlayPy folder (if needed)

## Getting Help

If you continue experiencing issues:

1. Check the GitHub Issues: https://github.com/fercunha/overlaypy/issues
2. Create a new issue with:
   - Windows version
   - Python version
   - Complete error message
   - Steps to reproduce the problem

## Windows-Specific Features

- **Click-through overlays:** Allows mouse clicks to pass through the overlay
- **Multiple monitor support:** Full support for multi-monitor setups
- **High DPI awareness:** Scales properly on high-resolution displays
- **Windows notifications:** Integration with Windows notification system (future feature)

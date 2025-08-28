# OverlayPy Debugging and Logging

This document explains how to use the comprehensive logging system in OverlayPy to debug issues, especially on Windows.

## 🔍 **Logging Features**

### **Automatic Logging**
- **Log Directory**: `logs/` folder (created automatically)
- **Log Files**: `overlaypy_YYYYMMDD_HHMMSS.log`
- **Content**: Detailed application behavior, system info, errors
- **Retention**: Manual cleanup (logs are kept indefinitely)

### **Log Levels**
- **DEBUG**: Detailed step-by-step execution
- **INFO**: General application flow and status
- **WARNING**: Non-fatal issues and fallbacks
- **ERROR**: Errors that may affect functionality

### **What Gets Logged**
- ✅ **System Information**: OS, Python version, hardware
- ✅ **Monitor Detection**: All displays and their properties
- ✅ **Windows API Calls**: Click-through, window handles, errors
- ✅ **Overlay Operations**: Creation, positioning, sizing
- ✅ **User Interactions**: Button clicks, setting changes
- ✅ **Error Details**: Stack traces, Windows error codes

## 🚀 **Quick Debugging**

### **Windows Users**

#### **Option 1: Debug Scripts (Recommended)**
```cmd
# Batch script - simple and reliable
debug-windows.bat

# PowerShell script - more features
debug-windows.ps1
debug-windows.ps1 -Verbose
debug-windows.ps1 -TestOnly
```

#### **Option 2: Manual Commands**
```cmd
# Test mode (exits after 3 seconds)
python overlay.py --test --debug

# Interactive mode with debug logging
python overlay.py --debug

# Set specific log level
python overlay.py --log-level DEBUG
```

### **macOS/Linux Users**
```bash
# Test mode
python overlay.py --test --debug

# Interactive debug mode
python overlay.py --debug

# Verbose logging
python overlay.py --log-level DEBUG
```

## 📋 **Command Line Options**

| Option | Description | Example |
|--------|-------------|---------|
| `--test` | Run test mode (auto-exit) | `python overlay.py --test` |
| `--debug` | Enable debug console output | `python overlay.py --debug` |
| `--log-level LEVEL` | Set log level | `python overlay.py --log-level ERROR` |

## 📁 **Log File Contents**

### **Startup Section**
```
2024-08-28 10:30:15 - INFO - OVERLAYPY STARTUP - SYSTEM INFORMATION
Platform: Windows-10-10.0.19041-SP0
System: Windows
Python version: 3.11.4
Detected 2 monitor(s):
  Monitor 1: Monitor(x=0, y=0, width=1920, height=1080, name='\\.\DISPLAY1')
  Monitor 2: Monitor(x=1920, y=0, width=1920, height=1080, name='\\.\DISPLAY2')
```

### **Overlay Creation**
```
2024-08-28 10:30:20 - INFO - Creating new overlay window...
2024-08-28 10:30:20 - DEBUG - ✓ Toplevel window created
2024-08-28 10:30:20 - DEBUG - ✓ Override redirect set
2024-08-28 10:30:20 - DEBUG - ✓ Topmost attribute set
```

### **Windows Click-Through**
```
2024-08-28 10:30:21 - INFO - Attempting to enable Windows click-through feature...
2024-08-28 10:30:21 - DEBUG - Overlay winfo_id: 123456789
2024-08-28 10:30:21 - DEBUG - GetParent result: 987654321
2024-08-28 10:30:21 - DEBUG - Current window style: 0x94000000
2024-08-28 10:30:21 - DEBUG - New window style: 0x940a0020
2024-08-28 10:30:21 - INFO - ✓ Click-through feature enabled successfully
```

### **Error Examples**
```
2024-08-28 10:30:25 - ERROR - Failed to create overlay window: [WinError 1400] Invalid window handle
2024-08-28 10:30:25 - WARNING - Click-through feature failed (overlay still functional): access denied
```

## 🔧 **Debugging Specific Issues**

### **Issue: Overlay Not Appearing**
**Check logs for:**
- Monitor detection failures
- Overlay window creation errors
- Positioning calculation problems

**Look for:**
```
ERROR - Failed to detect monitors
ERROR - Failed to create overlay window
ERROR - Failed to position overlay
```

### **Issue: Click-Through Not Working**
**Check logs for:**
- Windows API call failures
- Permission issues
- Window handle problems

**Look for:**
```
WARNING - Click-through feature failed
ERROR - GetParent returned 0
WARNING - SetWindowLongW returned 0
```

### **Issue: Multiple Monitor Problems**
**Check logs for:**
- Monitor detection results
- Positioning calculations
- Monitor selection issues

**Look for:**
```
INFO - Detected X monitor(s)
DEBUG - Selected monitor for positioning
ERROR - No matching monitor found
```

### **Issue: Application Crashes**
**Check logs for:**
- Import errors
- System compatibility issues
- Fatal exceptions

**Look for:**
```
ERROR - Fatal error in main
ImportError - No module named
Exception type: WindowsError
```

## 📊 **Debug Script Features**

### **debug-windows.bat**
- ✅ **Python Detection**: Verifies Python installation
- ✅ **Virtual Environment**: Auto-activates if available
- ✅ **Test Mode**: Runs 5-second automated test
- ✅ **Interactive Mode**: Optional manual testing
- ✅ **Output Capture**: Saves all output to timestamped file

### **debug-windows.ps1**
- ✅ **System Information**: Detailed hardware/software info
- ✅ **Multiple Test Modes**: Test-only, interactive-only, both
- ✅ **Verbose Output**: Optional detailed console output
- ✅ **Issue Detection**: Checks for common problems
- ✅ **Professional Output**: Colored, structured logging

## 🛠️ **Troubleshooting Steps**

### **1. Basic Debugging**
```cmd
# Run this first
debug-windows.bat
```

### **2. If Test Fails**
```cmd
# Get detailed output
python overlay.py --test --debug --log-level DEBUG
```

### **3. Check Log Files**
```cmd
# Look in logs directory
dir logs\
type logs\overlaypy_latest.log
```

### **4. Share Debug Information**
When reporting issues, include:
- Debug script output file
- Latest log file from `logs/` directory
- Windows version and Python version
- Description of expected vs actual behavior

## 📝 **Example Debug Session**

```cmd
C:\overlaypy> debug-windows.bat
[INFO] Starting OverlayPy Windows Debug Session
================================================

[INFO] Found Python 3.11.4
[INFO] Activating virtual environment...
[INFO] Debug output will be saved to: debug_20240828_103015.log

[INFO] Running OverlayPy in TEST MODE (5 second test)...
--------------------------------------------------------
[SUCCESS] Test mode completed successfully

Do you want to run in interactive mode for manual testing? (Y/N) y

[INFO] Running OverlayPy in INTERACTIVE MODE...
-----------------------------------------------
Press Ctrl+C to exit when done testing

# ... application runs, user tests functionality ...

[INFO] Debug session completed

Debug files created:
- debug_20240828_103015.log (this session)
- logs\overlaypy_20240828_103015.log (detailed application logs)
```

## 🔍 **Advanced Debugging**

### **Custom Log Analysis**
```python
# Search for specific errors
grep -i "error" logs/overlaypy_*.log

# Find Windows-specific issues
grep -i "windows\|click-through\|ctypes" logs/overlaypy_*.log

# Monitor detection problems
grep -i "monitor\|display" logs/overlaypy_*.log
```

### **Real-Time Monitoring**
```cmd
# Watch log file in real-time (Windows)
powershell Get-Content logs\overlaypy_latest.log -Wait

# Linux/macOS
tail -f logs/overlaypy_latest.log
```

This comprehensive logging system should help identify exactly what's happening when OverlayPy runs on Windows and where any issues occur!

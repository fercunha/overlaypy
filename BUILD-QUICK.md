# Building Windows Executables - Quick Guide

This document provides quick instructions for building Windows executables from OverlayPy.

## 🚀 **Quick Start**

### **Automated Build (Recommended)**
1. Push code to trigger GitHub Actions:
   ```bash
   git push origin main
   # OR create a tag for releases
   git tag v1.0.1
   git push origin v1.0.1
   ```
2. Download artifacts from GitHub Actions

### **Manual Build on Windows**

#### **Option 1: One-Click Build**
```cmd
# Download and run
build-windows.bat
```

#### **Option 2: PowerShell (Advanced)**
```powershell
# Run with options
.\build-windows.ps1 -Verbose
.\build-windows.ps1 -QuickBuild    # Skip portable version
.\build-windows.ps1 -SkipTests     # Skip application tests
```

#### **Option 3: Python Script**
```cmd
# Setup and build
python build-windows.py
```

## 📋 **What Gets Installed**

### **Runtime Dependencies** (from requirements.txt)
- `screeninfo` - Multi-monitor support
- `pyobjc` packages (macOS only)

### **Build Dependencies** (automatically installed)
- `pyinstaller>=6.0.0` - Creates executables
- `pillow>=10.0.0` - Icon support  
- `wheel` & `setuptools` - Build tools
- `auto-py-to-exe` (optional) - GUI tool

## 🔧 **Build Process**

Each build script performs these steps:

1. **Environment Setup**
   - ✅ Check Python 3.8+ installation
   - ✅ Create/activate virtual environment
   - ✅ Upgrade pip

2. **Dependency Installation**
   - ✅ Install runtime dependencies
   - ✅ Install build dependencies
   - ✅ Verify PyInstaller installation

3. **Icon Creation**
   - ✅ Generate professional application icon
   - ✅ Multiple sizes for Windows compatibility
   - ✅ Fallback for systems without Pillow

4. **Application Testing**
   - ✅ Test imports and basic functionality
   - ✅ Verify all dependencies are available

5. **Executable Creation**
   - ✅ Build single executable (`OverlayPy.exe`)
   - ✅ Build portable directory version (optional)
   - ✅ Include documentation and resources

6. **Release Package**
   - ✅ Create release folder with all files
   - ✅ Generate launcher scripts
   - ✅ Include documentation and README

## 📁 **Output Structure**

After building, you'll have:

```
dist/
├── OverlayPy.exe                    # Single executable (8-15 MB)
└── OverlayPy-Portable/              # Directory version
    ├── OverlayPy-Portable.exe       # Main executable
    ├── _internal/                   # Dependencies
    └── ...

release/                             # Distribution package
├── OverlayPy.exe                    # Single executable
├── OverlayPy-Portable/              # Portable version
├── OverlayPy-Launcher.bat          # Smart launcher
├── README-RELEASE.txt               # User instructions
├── README.md                        # General docs
├── WINDOWS.md                       # Windows help
└── install.bat                      # Installation script
```

## 🎯 **Which Version to Use?**

### **Single Executable (`OverlayPy.exe`)**
- ✅ **Best for**: Simple distribution, email sharing
- ✅ **Pros**: One file, easy to share
- ❌ **Cons**: Larger size, slower startup

### **Portable Directory (`OverlayPy-Portable/`)**
- ✅ **Best for**: Local use, faster performance
- ✅ **Pros**: Faster startup, smaller individual files
- ❌ **Cons**: Multiple files to manage

### **GitHub Actions (Automated)**
- ✅ **Best for**: Professional distribution, CI/CD
- ✅ **Pros**: Consistent builds, no Windows machine needed
- ❌ **Cons**: Requires GitHub repository

## 🛠️ **Build Script Options**

### **Batch Script (`build-windows.bat`)**
- Simple, works on any Windows system
- No parameters, builds everything
- Good for beginners

### **PowerShell Script (`build-windows.ps1`)**
- Advanced options and better error handling
- Colored output and progress indicators
- Professional build logs

```powershell
# Available parameters:
-SkipTests      # Skip application testing
-QuickBuild     # Only build single executable
-OutputDir      # Custom output directory  
-Verbose        # Detailed logging
```

### **Python Script (`build-windows.py`)**
- Cross-platform (works on macOS/Linux too)
- Most flexible and customizable
- Can be integrated into other Python workflows

## ⚠️ **Troubleshooting**

### **Common Issues**

**"Python not found"**
```cmd
# Install Python from python.org
# Make sure "Add to PATH" is checked during installation
```

**"PyInstaller failed"**
```cmd
# Try upgrading PyInstaller
pip install --upgrade pyinstaller
```

**"Large executable size"**
```python
# Add more exclusions in build script
--exclude-module matplotlib
--exclude-module numpy
--exclude-module pandas
```

**"Antivirus blocks executable"**
- Add exclusion for your build directory
- Consider code signing for distribution
- Submit to antivirus vendors for whitelisting

### **Performance Tips**

**Faster Builds**
```powershell
# Use QuickBuild for testing
.\build-windows.ps1 -QuickBuild -SkipTests
```

**Smaller Executables**
```python
# Add more exclusions
--exclude-module torch
--exclude-module tensorflow
--exclude-module jupyter
```

**Better Icons**
- Place custom `icon.ico` in project root
- Build scripts will use it automatically
- Must be proper Windows ICO format

## 📊 **Build Times & Sizes**

Typical results on modern Windows machine:

| Build Type | Time | Size | Best For |
|------------|------|------|----------|
| Single EXE | 30-60s | 8-15 MB | Distribution |
| Portable | 20-40s | 12-20 MB total | Local use |
| Both | 60-90s | - | Complete package |

## 🔗 **Next Steps**

After building:

1. **Test on clean Windows system**
2. **Create installer** (optional, see BUILD.md)
3. **Code sign** for professional distribution
4. **Upload to GitHub Releases**
5. **Share with users**

For detailed instructions, see [BUILD.md](BUILD.md)

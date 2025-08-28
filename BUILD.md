# Building Windows Executables for OverlayPy

This guide explains how to create Windows `.exe` files for OverlayPy, including cross-platform compilation from macOS.

## 🎯 **Quick Start - Automated Builds**

### **Method 1: GitHub Actions (Recommended)**

The easiest way to create Windows executables is through our automated GitHub Actions workflow:

1. **Push to main branch or create a tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Download from GitHub Actions:**
   - Go to your repository's "Actions" tab
   - Find the "Build Windows Executable" workflow
   - Download the artifacts

3. **Or create a release:**
   - Tags automatically create GitHub releases with downloadable executables

## 🔧 **Manual Building Methods**

### **Method 2: From Windows Machine**

If you have access to a Windows machine:

```cmd
# Clone and setup
git clone https://github.com/yourusername/overlaypy.git
cd overlaypy
install.bat

# Build executable
python build-windows.py
```

### **Method 3: From macOS using Docker**

```bash
# Build using Docker Windows container
docker build -f Dockerfile.windows -t overlaypy-windows .
docker run --rm -v $(pwd)/dist:/app/dist overlaypy-windows
```

### **Method 4: Cloud Build Services**

Use services like:
- **GitHub Codespaces** with Windows environment
- **Azure DevOps** with Windows agents  
- **AppVeyor** CI/CD
- **CircleCI** with Windows executors

## 📋 **Build Options Explained**

### **Single Executable (`--onefile`)**
- **Pros:** Single file, easy distribution
- **Cons:** Larger file size, slower startup
- **Best for:** Simple distribution, email sharing

### **One-Directory Bundle (`--onedir`)**
- **Pros:** Faster startup, smaller individual files
- **Cons:** Multiple files to distribute
- **Best for:** Installation packages, professional distribution

## 🛠️ **Advanced Configuration**

### **Custom PyInstaller Spec File**

For advanced builds, edit `overlay.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['overlay.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('WINDOWS.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'screeninfo',
    ],
    excludes=[
        'matplotlib',  # Exclude large unused libraries
        'numpy',
        'pandas',
    ],
)

exe = EXE(
    # ... configuration
    console=False,  # Hide console window
    icon='icon.ico',
)
```

### **Optimization Tips**

1. **Exclude unused modules:**
   ```bash
   pyinstaller --exclude-module matplotlib --exclude-module numpy overlay.py
   ```

2. **Use UPX compression:**
   ```bash
   pyinstaller --upx-dir /path/to/upx overlay.py
   ```

3. **Minimize dependencies:**
   - Remove unused imports
   - Use lighter alternatives where possible

## 🎨 **Creating Application Icons**

### **Automatic Icon Generation**

The build scripts automatically create an icon, but you can customize it:

```python
from PIL import Image, ImageDraw

# Create custom icon
size = (256, 256)
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Your custom design here
draw.rectangle([20, 20, 236, 236], fill=(70, 130, 180, 255))
draw.text((100, 115), 'OVL', fill=(255, 255, 255, 255))

# Save as Windows icon
img.save('custom-icon.ico', format='ICO', 
         sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
```

### **Using Existing Icons**

Place your `.ico` file in the project root and update the build command:

```bash
pyinstaller --icon=my-icon.ico overlay.py
```

## 📦 **Distribution Strategies**

### **1. Simple Distribution**
- Upload `.exe` to GitHub Releases
- Share direct download links
- Email single executable file

### **2. Installer Package**

Create an installer using:

#### **NSIS (Nullsoft Scriptable Install System)**
```nsis
; installer.nsi
!define APPNAME "OverlayPy"
!define VERSION "1.0.0"

OutFile "OverlayPy-Installer.exe"
InstallDir "$PROGRAMFILES\${APPNAME}"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File "dist\OverlayPy.exe"
    File "README.md"
    File "WINDOWS.md"
    
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\OverlayPy.exe"
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\OverlayPy.exe"
SectionEnd
```

#### **Inno Setup**
```pascal
[Setup]
AppName=OverlayPy
AppVersion=1.0.0
DefaultDirName={pf}\OverlayPy
OutputBaseFilename=OverlayPy-Setup

[Files]
Source: "dist\OverlayPy.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"

[Icons]
Name: "{group}\OverlayPy"; Filename: "{app}\OverlayPy.exe"
Name: "{desktop}\OverlayPy"; Filename: "{app}\OverlayPy.exe"
```

### **3. Microsoft Store**

For Microsoft Store distribution:
1. Package using `msix-packaging-tool`
2. Submit through Partner Center
3. Requires developer account ($19/year)

## 🔒 **Code Signing (Optional)**

For professional distribution, sign your executable:

### **Self-Signed Certificate (Free)**
```bash
# Create certificate
makecert -sv mykey.pvk -n "CN=Your Company" mycert.cer
pvk2pfx -pvk mykey.pvk -spc mycert.cer -pfx mycert.pfx

# Sign executable
signtool sign /f mycert.pfx /p password dist/OverlayPy.exe
```

### **Commercial Certificate**
Purchase from providers like:
- DigiCert
- Sectigo
- GlobalSign

## 🧪 **Testing Your Executable**

### **Testing Checklist**
- [ ] Runs on clean Windows machine
- [ ] No Python installation required
- [ ] All features work correctly
- [ ] Multiple monitor support
- [ ] Click-through functionality
- [ ] Auto-hide timer
- [ ] Proper error handling

### **Test Environments**
- Windows 10 (minimum supported)
- Windows 11
- Different screen resolutions
- Multiple monitor setups
- Various Windows themes

## 🔍 **Troubleshooting Build Issues**

### **Common Problems**

#### **Missing DLLs**
```bash
# Include system DLLs
pyinstaller --collect-all tkinter overlay.py
```

#### **Import Errors**
```bash
# Add hidden imports
pyinstaller --hidden-import=screeninfo overlay.py
```

#### **Large File Size**
```bash
# Exclude unused modules
pyinstaller --exclude-module=matplotlib overlay.py
```

#### **Antivirus False Positives**
- Submit to antivirus vendors for whitelisting
- Use code signing to reduce false positives
- Build with older PyInstaller versions if needed

## 📊 **Build Comparison**

| Method | Platform | Ease | Size | Speed | Notes |
|--------|----------|------|------|-------|-------|
| GitHub Actions | Any | ⭐⭐⭐⭐⭐ | Medium | Fast | Recommended |
| Windows Machine | Windows | ⭐⭐⭐⭐ | Medium | Fast | Direct build |
| Docker | Any | ⭐⭐⭐ | Large | Medium | Complex setup |
| Cross-compile | macOS/Linux | ⭐⭐ | Medium | Medium | Limited support |

## 🚀 **Next Steps**

1. **Choose your build method** based on your needs
2. **Test thoroughly** on target Windows systems  
3. **Consider code signing** for professional distribution
4. **Create installer** for easier user experience
5. **Set up CI/CD** for automated builds

For questions or issues, check the [GitHub Issues](https://github.com/fercunha/overlaypy/issues) or create a new issue.

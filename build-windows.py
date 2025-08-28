#!/usr/bin/env python3
"""
Build script for creating Windows executable from macOS
Uses PyInstaller with cross-compilation support
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def install_build_dependencies():
    """Install PyInstaller and other build dependencies."""
    print("📦 Installing build dependencies...")
    
    dependencies = [
        "pyinstaller>=5.13.0",
        "auto-py-to-exe>=2.38.0",  # Optional GUI tool
        "pillow>=10.0.0",          # For icon support
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True, text=True)
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
    
    return True


def create_spec_file():
    """Create PyInstaller spec file for better control."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

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
        'ctypes',
        'platform',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'jupyter',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OverlayPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)
'''
    
    with open('overlay.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Created overlay.spec file")


def build_executable():
    """Build the Windows executable."""
    print("🔨 Building Windows executable...")
    
    # Create spec file first
    create_spec_file()
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "overlay.spec"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        print(f"📁 Executable location: dist/OverlayPy.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def build_with_onedir():
    """Build one-directory bundle (alternative to single exe)."""
    print("🔨 Building Windows one-directory bundle...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "OverlayPy",
        "--add-data", "README.md:.",
        "--add-data", "WINDOWS.md:.",
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "overlay.py"
    ]
    
    if Path('icon.ico').exists():
        cmd.extend(["--icon", "icon.ico"])
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ One-directory build completed!")
        print(f"📁 Application folder: dist/OverlayPy/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_icon():
    """Create a simple icon for the application."""
    print("🎨 Creating application icon...")
    
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        size = (256, 256)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple overlay-like design
        margin = 20
        draw.rectangle([margin, margin, size[0]-margin, size[1]-margin], 
                      fill=(70, 130, 180, 255), outline=(25, 25, 112, 255), width=4)
        
        # Add text
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("Arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        text = "OVL"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2
        
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
        
        # Save as ICO
        img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        print("✅ Created icon.ico")
        return True
        
    except ImportError:
        print("⚠️  Pillow not available, skipping icon creation")
        return False
    except Exception as e:
        print(f"⚠️  Icon creation failed: {e}")
        return False


def main():
    """Main build process."""
    print("🚀 OverlayPy Windows Executable Builder")
    print("=" * 50)
    
    if platform.system() != "Darwin":
        print("⚠️  This script is designed to run on macOS")
        print("   It should still work on other platforms")
    
    # Install dependencies
    if not install_build_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Create icon
    create_icon()
    
    # Ask user which build type they want
    print("\n📋 Build Options:")
    print("1. Single executable file (larger, slower start)")
    print("2. One-directory bundle (smaller, faster start)")
    print("3. Both")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    success = False
    
    if choice in ["1", "3"]:
        print("\n" + "="*50)
        print("Building single executable...")
        success = build_executable()
    
    if choice in ["2", "3"]:
        print("\n" + "="*50)
        print("Building one-directory bundle...")
        success = build_with_onedir() or success
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("\n📦 Output files:")
        
        if Path("dist/OverlayPy.exe").exists():
            size = Path("dist/OverlayPy.exe").stat().st_size / (1024*1024)
            print(f"   Single executable: dist/OverlayPy.exe ({size:.1f} MB)")
        
        if Path("dist/OverlayPy").exists():
            print(f"   One-directory bundle: dist/OverlayPy/")
        
        print("\n📋 Next steps:")
        print("1. Test the executable on a Windows machine")
        print("2. Consider code signing for distribution")
        print("3. Create an installer using NSIS or Inno Setup")
        
    else:
        print("\n❌ Build failed!")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

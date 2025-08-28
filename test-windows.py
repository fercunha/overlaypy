#!/usr/bin/env python3
"""
Windows compatibility test script for OverlayPy
Tests all Windows-specific functionality without GUI
"""

import sys
import platform
import subprocess
from pathlib import Path


def test_python_version():
    """Test if Python version is compatible."""
    print("Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old (need 3.7+)")
        return False


def test_platform_detection():
    """Test platform detection."""
    print("Testing platform detection...")
    system = platform.system()
    print(f"✅ Detected platform: {system}")
    
    if system == "Windows":
        print("✅ Windows-specific features will be enabled")
        return True
    else:
        print("ℹ️  Running on non-Windows platform")
        return True


def test_tkinter_import():
    """Test if tkinter can be imported."""
    print("Testing tkinter import...")
    try:
        import tkinter as tk
        print("✅ tkinter imported successfully")
        
        # Test basic tkinter functionality
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.quit()
        print("✅ tkinter basic functionality works")
        return True
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  tkinter import succeeded but basic test failed: {e}")
        return False


def test_screeninfo_import():
    """Test if screeninfo can be imported."""
    print("Testing screeninfo import...")
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        print(f"✅ screeninfo imported successfully")
        print(f"✅ Found {len(monitors)} monitor(s)")
        for i, monitor in enumerate(monitors):
            print(f"   Monitor {i+1}: {monitor.width}x{monitor.height}")
        return True
    except ImportError as e:
        print(f"❌ screeninfo import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  screeninfo import succeeded but monitor detection failed: {e}")
        return False


def test_ctypes_availability():
    """Test if ctypes is available for Windows features."""
    print("Testing ctypes availability...")
    try:
        import ctypes
        print("✅ ctypes imported successfully")
        
        if platform.system() == "Windows":
            # Test Windows-specific ctypes functions
            try:
                user32 = ctypes.windll.user32
                print("✅ Windows user32.dll accessible")
                return True
            except Exception as e:
                print(f"⚠️  Windows-specific ctypes functions failed: {e}")
                return False
        else:
            print("ℹ️  Not on Windows, skipping Windows-specific ctypes tests")
            return True
    except ImportError as e:
        print(f"❌ ctypes import failed: {e}")
        return False


def test_virtual_environment():
    """Test if running in virtual environment."""
    print("Testing virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        venv_path = Path(sys.prefix)
        print(f"   Virtual env path: {venv_path}")
        return True
    else:
        print("⚠️  Not running in virtual environment (not required, but recommended)")
        return True


def test_file_permissions():
    """Test if we can write files (for overlay positioning)."""
    print("Testing file permissions...")
    try:
        test_file = Path("test_write_permissions.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("✅ File write permissions work")
        return True
    except Exception as e:
        print(f"❌ File write test failed: {e}")
        return False


def main():
    """Run all compatibility tests."""
    print("=" * 50)
    print("OverlayPy Windows Compatibility Test")
    print("=" * 50)
    print()
    
    tests = [
        test_python_version,
        test_platform_detection,
        test_tkinter_import,
        test_screeninfo_import,
        test_ctypes_availability,
        test_virtual_environment,
        test_file_permissions,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
        print()
    
    print("=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! OverlayPy should work perfectly on this system.")
    elif passed >= total - 1:
        print("✅ Most tests passed. OverlayPy should work with minor limitations.")
    else:
        print("⚠️  Some tests failed. OverlayPy may have limited functionality.")
        print("   Check the error messages above for specific issues.")
    
    print("\nTo run OverlayPy:")
    if platform.system() == "Windows":
        print("   Double-click: run-overlay.bat")
        print("   Or run: localvenv\\Scripts\\activate && python overlay.py")
    else:
        print("   Run: source localvenv/bin/activate && python overlay.py")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

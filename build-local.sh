#!/bin/bash

# Simple script to build Windows .exe from macOS using PyInstaller
# Note: This creates a macOS executable, not Windows. See other methods for true cross-compilation.

echo "🚀 Building OverlayPy executable..."
echo "Note: This builds for macOS. For Windows .exe, use GitHub Actions or Docker."
echo

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Not in virtual environment. Activating..."
    if [ -d "localvenv" ]; then
        source localvenv/bin/activate
    else
        echo "❌ Virtual environment not found. Run install.sh first."
        exit 1
    fi
fi

# Install PyInstaller if not already installed
echo "📦 Installing PyInstaller..."
pip install pyinstaller pillow

# Create a simple icon (macOS version)
echo "🎨 Creating application icon..."
python3 << 'EOF'
try:
    from PIL import Image, ImageDraw
    
    # Create a simple icon
    size = (512, 512)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple overlay-like design
    margin = 40
    draw.rectangle([margin, margin, size[0]-margin, size[1]-margin], 
                  fill=(70, 130, 180, 255), outline=(25, 25, 112, 255), width=8)
    
    # Add text
    try:
        font_size = 120
        text = "OVL"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2
        
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 255))
    except:
        # Fallback if font loading fails
        draw.text((200, 230), "OVL", fill=(255, 255, 255, 255))
    
    # Save as different formats
    img.save('icon.png', format='PNG')
    img.save('icon.icns', format='ICNS')  # macOS
    print("✅ Created icon files")
    
except ImportError:
    print("⚠️  Pillow not available, using default icon")
except Exception as e:
    print(f"⚠️  Icon creation failed: {e}")
EOF

# Build the application
echo "🔨 Building application..."

# For macOS
pyinstaller --onefile --windowed --name OverlayPy --icon icon.icns overlay.py

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "📁 Executable location: dist/OverlayPy"
    echo
    echo "📋 For Windows .exe files:"
    echo "   1. Use GitHub Actions (automatic on push/tag)"
    echo "   2. Use the build-windows.py script on a Windows machine"
    echo "   3. Use Docker with Windows containers"
    echo
    echo "🚀 To test the macOS version:"
    echo "   ./dist/OverlayPy"
else
    echo "❌ Build failed!"
    exit 1
fi

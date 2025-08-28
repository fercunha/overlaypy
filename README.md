# 🖥️ OverlayPy

A powerful and customizable Python application for creating text overlays on your desktop. Perfect for presentations, gaming, streaming, status updates, and accessibility needs.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎨 **Customizable Text Display**
- **Font sizes from 12pt to 240pt** - Perfect for any display size
- **Custom message input** - Display any text you want
- **Adjustable padding** - Control spacing around your text
- **Bold white text on black background** - High contrast for maximum readability

### 🖥️ **Multi-Monitor Support**
- **Automatic monitor detection** - See all connected displays
- **Smart monitor names** - Shows resolution and display names
- **Flexible positioning** - Bottom-left corner placement by default

### ⏱️ **Timer Controls**
- **Auto-hide timer** - Set custom duration (default: 60 seconds)
- **Timer toggle** - Enable/disable auto-hide functionality
- **Manual control** - Show/hide overlay anytime with button click

### 🎛️ **Professional Interface**
- **Always on top** - Control window stays accessible
- **Scrollable interface** - Clean, organized layout
- **Intuitive controls** - Easy-to-use GUI with clear labels
- **Real-time updates** - Changes apply immediately

### 🌐 **Cross-Platform**
- **macOS** - Full support with native scrolling
- **Windows** - Includes click-through functionality
- **Linux** - Compatible with X11 environments

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Git (for cloning the repository)

### 🔧 Automated Installation (Recommended)

The easiest way to get started is using our installation script:

1. **Clone the repository**
   ```bash
   git clone https://github.com/fercunha/overlaypy.git
   cd overlaypy
   ```

2. **Run the installation script**
   ```bash
   ./install.sh
   ```

3. **Follow the on-screen instructions and then run**
   ```bash
   source localvenv/bin/activate
   python overlay.py
   ```

#### 📋 Installation Script Features
- ✅ **Automatic OS detection** (macOS, Linux, Windows)
- ✅ **Python version verification**
- ✅ **macOS Tkinter setup** (via Homebrew if available)
- ✅ **Virtual environment creation**
- ✅ **Dependency installation**
- ✅ **Installation testing**
- ✅ **Colored output** for easy reading

#### 🛠️ Script Options
```bash
./install.sh [OPTIONS]

Options:
  -h, --help     Show help message
  -v, --verbose  Enable verbose output  
  --clean        Clean install (remove existing venv)
```

### 📱 Manual Installation

If you prefer to install manually or the script doesn't work for your system:

1. **Clone the repository**
   ```bash
   git clone https://github.com/fercunha/overlaypy.git
   cd overlaypy
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python3 -m venv localvenv
   source localvenv/bin/activate  # On Windows: localvenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python overlay.py
   ```

### 🍎 macOS Additional Setup
If you encounter Tkinter issues on macOS:
```bash
brew install python-tk
# Then recreate your virtual environment with the Homebrew Python
/opt/homebrew/bin/python3 -m venv localvenv
source localvenv/bin/activate
pip install -r requirements.txt
```

## 📋 Usage

### Basic Usage
1. **Launch** the application: `python overlay.py`
2. **Enter your message** in the text field
3. **Select monitor** from the dropdown (if multiple displays)
4. **Choose font size** (12pt - 240pt available)
5. **Set padding** for spacing around text
6. **Configure timer** or disable auto-hide
7. **Click "Show Overlay"** to display your text

### Advanced Features

#### Timer Settings
- ✅ **Enable timer**: Check "Auto-hide after" box
- ⏱️ **Set duration**: Enter seconds in the timer field
- ♾️ **Persistent display**: Uncheck timer for manual control only

#### Font Size Options
- **Small notifications**: 12-24pt
- **Standard overlays**: 30-48pt  
- **Large displays**: 60-96pt
- **Massive text**: 120-240pt (perfect for projectors/large screens)

#### Monitor Selection
- **Automatic detection**: All connected monitors appear in dropdown
- **Smart labeling**: Shows monitor name and resolution
- **Easy switching**: Change monitors without restarting overlay

## 🎯 Use Cases

### 🎮 **Gaming**
- Display game status, timers, or reminders
- Show streaming information for viewers
- Create custom HUD elements

### 📊 **Presentations**
- Add large, visible notes or reminders
- Display timing information
- Show key points during demos

### 💼 **Work & Productivity**
- Status updates during video calls
- Reminder notifications
- Progress indicators for long tasks

### ♿ **Accessibility**
- Large text for vision assistance
- High contrast display for readability
- Customizable sizing for different needs

### 🎥 **Content Creation**
- Streaming overlays for live broadcasts
- Video recording annotations
- Tutorial highlighting

## 🛠️ Technical Details

### Dependencies
```
Cython==3.1.3
pyobjc-core==11.1
pyobjc-framework-Cocoa==11.1
screeninfo==0.8.1
```

### Platform-Specific Features
- **Windows**: Click-through overlay support
- **macOS**: Native scrolling and window management
- **Linux**: Standard Tkinter functionality

### File Structure
```
overlaypy/
├── overlay.py          # Main application
├── install.sh          # Automated installation script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── localvenv/         # Virtual environment (created during setup)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly on your platform
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

If you encounter any issues or have suggestions:
1. Check existing [Issues](https://github.com/fercunha/overlaypy/issues)
2. Create a new issue with detailed description
3. Include your OS, Python version, and error messages

## 🚀 Future Enhancements

- [ ] Color customization options
- [ ] Multiple overlay support
- [ ] Transparency controls
- [ ] Custom fonts selection
- [ ] Keyboard shortcuts
- [ ] Configuration file support
- [ ] System tray integration

---

**Made with ❤️ for the desktop overlay community**

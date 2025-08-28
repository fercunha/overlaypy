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
- **Flexible corner positioning** - Choose from all 4 corners (default: bottom-left)
- **Real-time monitor switching** - Change monitors and overlay moves instantly

### ⏱️ **Timer Controls**
- **Auto-hide timer** - Set custom duration (default: 60 seconds)
- **Timer toggle** - Enable/disable auto-hide functionality
- **Manual control** - Show/hide overlay anytime with button click
- **Real-time timer updates** - Changes to timer settings apply instantly while overlay is visible

### 🎛️ **Professional Interface**
- **Always on top** - Control window stays accessible
- **Scrollable interface** - Clean, organized layout with side-by-side controls
- **Intuitive controls** - Easy-to-use GUI with clear labels
- **Real-time updates** - All settings (except message text) apply instantly
- **Side-by-side layout** - Font size, position, and padding controls organized horizontally

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

### 🪟 Windows Installation

For Windows users, we provide dedicated installation scripts:

#### **Option 1: Batch Script (Easiest)**
```cmd
git clone https://github.com/fercunha/overlaypy.git
cd overlaypy
install.bat
```

#### **Option 2: PowerShell Script (Advanced)**
```powershell
git clone https://github.com/fercunha/overlaypy.git
cd overlaypy
powershell -ExecutionPolicy Bypass -File install.ps1
```

#### **Running on Windows**
- **Quick start:** Double-click `run-overlay.bat`
- **Manual:** `localvenv\Scripts\activate` then `python overlay.py`

#### **Windows Features**
- ✅ **Click-through overlays** - Mouse clicks pass through overlay
- ✅ **High DPI support** - Scales properly on high-resolution displays  
- ✅ **Multi-monitor support** - Full support for multiple displays
- ✅ **Windows integration** - Native Windows behavior

📋 **Troubleshooting Windows issues?** See [WINDOWS.md](WINDOWS.md) for detailed solutions.

### 📱 Manual Installation

If you prefer to install manually or the script doesn't work for your system:

1. **Clone the repository**
   ```bash
   git clone https://github.com/fercunha/overlaypy.git
   cd overlaypy
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   # macOS/Linux
   python3 -m venv localvenv
   source localvenv/bin/activate
   
   # Windows
   python -m venv localvenv
   localvenv\Scripts\activate
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
3. **Configure settings** using the side-by-side controls:
   - **Font Size**: Select from 12pt to 240pt (updates in real-time)
   - **Position**: Choose corner placement (updates in real-time)
   - **Padding**: Adjust spacing around text (updates in real-time)
4. **Select monitor** from the dropdown (switches in real-time if multiple displays)
5. **Configure timer** settings (apply in real-time)
6. **Click "Show Overlay"** to display your text

### Real-Time Features
- ✅ **Font size changes**: Instant preview when adjusting size
- ✅ **Position changes**: Overlay moves immediately when selecting new corner
- ✅ **Padding adjustments**: Spacing updates as you type
- ✅ **Monitor switching**: Overlay relocates instantly to new display
- ✅ **Timer changes**: Auto-hide timer resets when you modify settings
- ℹ️ **Message text**: Only updates when clicking "Show Overlay" (intentional)

### Advanced Features

#### Timer Settings
- ✅ **Enable timer**: Check "Auto-hide after" box (applies instantly)
- ⏱️ **Set duration**: Enter seconds in the timer field (updates in real-time)
- ♾️ **Persistent display**: Uncheck timer for manual control only
- 🔄 **Smart updates**: Timer automatically resets when you change settings

#### Font Size Options
- **Small notifications**: 12-24pt
- **Standard overlays**: 30-48pt  
- **Large displays**: 60-96pt
- **Massive text**: 120-240pt (perfect for projectors/large screens)
- **Live preview**: See changes instantly as you adjust

#### Monitor & Position Management
- **Automatic detection**: All connected monitors appear in dropdown
- **Smart labeling**: Shows monitor name and resolution
- **Instant switching**: Change monitors and overlay moves immediately
- **Corner positioning**: All 4 corners available with real-time updates
- **Precise placement**: Overlay appears in correct position from the start

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
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make your changes
5. Run code quality checks: `./check-code.sh`
6. Test thoroughly on your platform
7. Submit a pull request

### Code Quality Tools
This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting and style checking
- **pylint**: Comprehensive code analysis
- **mypy**: Type checking
- **bandit**: Security vulnerability scanning
- **safety**: Dependency vulnerability checking
- **pytest**: Unit testing
- **radon**: Code complexity analysis

### Running Quality Checks Locally
```bash
# Run all checks at once
./check-code.sh

# Or run individual tools
black .                    # Format code
isort .                    # Sort imports
flake8 .                   # Lint code
pylint *.py               # Comprehensive analysis
mypy .                    # Type checking
bandit -r .               # Security check
safety check              # Dependency vulnerabilities
pytest                    # Run tests
```

### GitHub Actions
The repository includes comprehensive CI/CD workflows:
- **Code Quality & Security**: Runs on every push and PR
- **Multi-Python Testing**: Tests against Python 3.8-3.12
- **Automated Security Scanning**: Bandit and Safety checks
- **Code Complexity Analysis**: Radon, Xenon, and Vulture
- **Artifact Upload**: Security reports available for download

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
- [ ] Animation effects
- [ ] Custom positioning (not just corners)
- [ ] Text formatting options (italics, underline)

## 🎉 Recent Updates

### v2.0 - Real-Time Experience
- ✅ **Real-time updates** - All settings except message text update instantly
- ✅ **Side-by-side layout** - Cleaner, more organized control interface
- ✅ **Monitor switching** - Instant overlay relocation between displays
- ✅ **Timer real-time** - Auto-hide settings apply immediately
- ✅ **Improved positioning** - Accurate placement from the start
- ✅ **Duplicate control removal** - Cleaner, streamlined interface

---

**Made with ❤️ for the desktop overlay community**

> ⚡ **Disclaimer**: This app was *vibe coded* - built with passion, creativity, and a "let's see what happens" attitude. It works great, but don't be surprised if you find some delightfully unconventional solutions! 🎨✨

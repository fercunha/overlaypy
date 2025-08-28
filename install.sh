#!/bin/bash

# OverlayPy Installation Script
# This script automates the setup process for OverlayPy

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Main installation function
install_overlaypy() {
    echo ""
    echo "🖥️  OverlayPy Installation Script"
    echo "================================="
    echo ""

    # Detect operating system
    OS=$(detect_os)
    print_status "Detected OS: $OS"

    # Check Python installation
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.7+ first."
        if [[ "$OS" == "macos" ]]; then
            print_status "On macOS, you can install Python with: brew install python"
        elif [[ "$OS" == "linux" ]]; then
            print_status "On Linux, try: sudo apt-get install python3 python3-pip python3-venv"
        fi
        exit 1
    fi

    # Get Python version
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Found Python $PYTHON_VERSION"

    # macOS specific setup for Tkinter
    if [[ "$OS" == "macos" ]]; then
        print_status "Setting up macOS environment..."
        
        # Check if Homebrew is installed
        if command_exists brew; then
            print_status "Installing python-tk via Homebrew..."
            if brew list python-tk@3.13 >/dev/null 2>&1; then
                print_success "python-tk is already installed"
            else
                brew install python-tk || {
                    print_warning "Failed to install python-tk via Homebrew"
                    print_status "Continuing with system Python..."
                }
            fi
            
            # Use Homebrew Python if available
            if [[ -f "/opt/homebrew/bin/python3" ]]; then
                PYTHON_CMD="/opt/homebrew/bin/python3"
                print_status "Using Homebrew Python: $PYTHON_CMD"
            else
                PYTHON_CMD="python3"
            fi
        else
            print_warning "Homebrew not found. Using system Python."
            print_status "If you encounter Tkinter issues, install Homebrew and run this script again."
            PYTHON_CMD="python3"
        fi
    else
        PYTHON_CMD="python3"
    fi

    # Create virtual environment
    print_status "Creating virtual environment..."
    if [[ -d "localvenv" ]]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf localvenv
    fi

    $PYTHON_CMD -m venv localvenv || {
        print_error "Failed to create virtual environment"
        exit 1
    }

    # Activate virtual environment
    print_status "Activating virtual environment..."
    source localvenv/bin/activate || {
        print_error "Failed to activate virtual environment"
        exit 1
    }

    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip

    # Install dependencies
    print_status "Installing dependencies..."
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt || {
            print_error "Failed to install dependencies"
            exit 1
        }
    else
        print_warning "requirements.txt not found. Installing basic dependencies..."
        pip install screeninfo
        if [[ "$OS" == "macos" ]]; then
            pip install pyobjc-core pyobjc-framework-Cocoa
        fi
    fi

    # Test the installation
    print_status "Testing installation..."
    python -c "import tkinter; import screeninfo; print('All dependencies OK')" || {
        print_error "Installation test failed. Some dependencies may be missing."
        exit 1
    }

    print_success "Installation completed successfully!"
    echo ""
    echo "🚀 Quick Start:"
    echo "   1. Activate the virtual environment: source localvenv/bin/activate"
    echo "   2. Run the application: python overlay.py"
    echo ""
    echo "📚 For more information, see the README.md file"
    echo ""
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose output"
    echo "  --clean        Clean install (remove existing venv)"
    echo ""
    echo "This script will:"
    echo "  • Check Python installation"
    echo "  • Set up platform-specific dependencies"
    echo "  • Create a virtual environment"
    echo "  • Install required packages"
    echo "  • Test the installation"
}

# Parse command line arguments
VERBOSE=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Enable verbose mode if requested
if [[ "$VERBOSE" == "true" ]]; then
    set -x
fi

# Clean install if requested
if [[ "$CLEAN" == "true" ]]; then
    print_status "Performing clean install..."
    rm -rf localvenv
fi

# Run installation
install_overlaypy

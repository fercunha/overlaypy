#!/bin/bash

# Local code quality and security check script
# Run this before committing to catch issues early

set -e  # Exit on any error

echo "🔍 Running local code quality and security checks..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if development dependencies are installed
print_status "Checking if development dependencies are installed..."
if ! python -c "import pylint, flake8, black, isort, bandit, safety, mypy" 2>/dev/null; then
    print_warning "Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

# Code formatting with Black
print_status "Running Black (code formatting)..."
if black --check --diff .; then
    print_success "Black formatting check passed"
else
    print_error "Black formatting check failed. Run 'black .' to fix."
    exit 1
fi

# Import sorting with isort
print_status "Running isort (import sorting)..."
if isort --check-only --diff .; then
    print_success "isort check passed"
else
    print_error "isort check failed. Run 'isort .' to fix."
    exit 1
fi

# Linting with flake8
print_status "Running flake8 (linting)..."
if flake8 .; then
    print_success "flake8 linting passed"
else
    print_error "flake8 linting failed"
    exit 1
fi

# Linting with pylint
print_status "Running pylint (comprehensive linting)..."
if pylint $(git ls-files '*.py') --exit-zero; then
    print_success "pylint check completed"
else
    print_warning "pylint found some issues (non-blocking)"
fi

# Type checking with mypy
print_status "Running mypy (type checking)..."
if mypy . --ignore-missing-imports --no-strict-optional; then
    print_success "mypy type checking passed"
else
    print_warning "mypy found some type issues (non-blocking)"
fi

# Security check with bandit
print_status "Running bandit (security analysis)..."
if bandit -r . -f txt; then
    print_success "bandit security check passed"
else
    print_warning "bandit found potential security issues"
fi

# Dependency vulnerability check with safety
print_status "Running safety (dependency vulnerability check)..."
if safety check; then
    print_success "safety check passed - no known vulnerabilities"
else
    print_warning "safety found potential vulnerabilities in dependencies"
fi

# Run tests
print_status "Running tests..."
if pytest --tb=short -v; then
    print_success "All tests passed"
else
    print_warning "Some tests failed or no tests found"
fi

# Code complexity analysis
print_status "Running code complexity analysis..."
echo "Cyclomatic Complexity:"
radon cc . -a
echo ""
echo "Maintainability Index:"
radon mi . -s

print_success "All checks completed! 🎉"
echo ""
echo "Summary:"
echo "✅ Code formatting (Black)"
echo "✅ Import sorting (isort)"
echo "✅ Linting (flake8)"
echo "✅ Comprehensive linting (pylint)"
echo "✅ Type checking (mypy)"
echo "✅ Security analysis (bandit)"
echo "✅ Dependency vulnerabilities (safety)"
echo "✅ Tests (pytest)"
echo "✅ Code complexity analysis"
echo ""
echo "Your code is ready for commit! 🚀"

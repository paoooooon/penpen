#!/bin/bash
# Install script for penpen CLI tool
# Usage: ./install.sh [OPTIONS]
#
# Options:
#   --skip-venv    Skip virtual environment creation (use existing)
#   -h, --help     Show this help message

set -e

# Default values
SKIP_VENV=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        -h|--help)
            echo "Install script for penpen CLI tool"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-venv    Skip virtual environment creation (use existing)"
            echo "  -h, --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "=== penpen Installer ==="
echo ""

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    elif command -v python &> /dev/null; then
        PYTHON_CMD=python
    else
        echo "Error: Python is not installed"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo "Using Python $PYTHON_VERSION"

    # Check Python version >= 3.10
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
        echo "Error: Python 3.10 or higher is required"
        exit 1
    fi
}

# Check and install sqlite3 command
check_sqlite3() {
    if command -v sqlite3 &> /dev/null; then
        echo "sqlite3 is already installed"
        return 0
    fi

    echo "sqlite3 command not found, installing..."

    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y sqlite3
    elif command -v apk &> /dev/null; then
        apk add --no-cache sqlite
    elif command -v yum &> /dev/null; then
        yum install -y sqlite
    elif command -v dnf &> /dev/null; then
        dnf install -y sqlite
    elif command -v pacman &> /dev/null; then
        pacman -S --noconfirm sqlite
    elif command -v brew &> /dev/null; then
        brew install sqlite
    else
        echo "Error: Could not install sqlite3. Please install it manually."
        exit 1
    fi

    if command -v sqlite3 &> /dev/null; then
        echo "sqlite3 installed successfully"
    else
        echo "Error: sqlite3 installation failed"
        exit 1
    fi
}

# Create and activate virtual environment
setup_venv() {
    if [ "$SKIP_VENV" = true ]; then
        echo "Skipping virtual environment creation (--skip-venv)"
        if [ -d "$SCRIPT_DIR/.venv" ]; then
            source "$SCRIPT_DIR/.venv/bin/activate"
            echo "Activated existing virtual environment"
        else
            echo "Warning: --skip-venv used but no .venv directory found"
        fi
        return
    fi

    if [ -d "$SCRIPT_DIR/.venv" ]; then
        echo "Virtual environment already exists, activating..."
        source "$SCRIPT_DIR/.venv/bin/activate"
    else
        echo "Creating virtual environment..."
        $PYTHON_CMD -m venv "$SCRIPT_DIR/.venv"
        source "$SCRIPT_DIR/.venv/bin/activate"
        echo "Virtual environment created and activated"
    fi
}

# Install Python dependencies
install_deps() {
    echo ""
    echo "Installing dependencies..."
    pip install --upgrade pip

    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        pip install -r "$SCRIPT_DIR/requirements.txt"
    fi

    # Install the penpen package in development mode
    if [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
        pip install -e "$SCRIPT_DIR"
        echo "penpenパッケージをインストールしました"
    fi

    echo "Dependencies installed successfully"
}

# Main execution
main() {
    check_python
    check_sqlite3
    setup_venv
    install_deps

    echo ""
    echo "=== Installation Complete ==="
    echo ""
    echo "To activate the virtual environment, run:"
    echo "  source .venv/bin/activate"
    echo ""
    echo "Usage:"
    echo "  penpen --help"
    echo "  penpen todo -m \"タスク内容\""
    echo "  penpen commit"
    echo ""
}

main
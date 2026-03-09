#!/bin/bash
# Install script for OpenAPI Python Client project
# Usage: ./install.sh [OPTIONS]
#
# Options:
#   --skip-venv    Skip virtual environment creation (use existing)
#   --skip-client  Skip client generation
#   --api-url      API URL for downloading OpenAPI spec (default: http://172.17.0.1:10000)
#   -h, --help     Show this help message

set -e

# Default values
SKIP_VENV=false
SKIP_CLIENT=false
API_URL="http://172.17.0.1:10000"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        --skip-client)
            SKIP_CLIENT=true
            shift
            ;;
        --api-url)
            API_URL="$2"
            shift 2
            ;;
        -h|--help)
            echo "Install script for OpenAPI Python Client project"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-venv    Skip virtual environment creation (use existing)"
            echo "  --skip-client  Skip client generation"
            echo "  --api-url      API URL for downloading OpenAPI spec"
            echo "                 (default: http://172.17.0.1:10000)"
            echo "  -h, --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "=== OpenAPI Python Client Installer ==="
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

    # Install openapi-python-client for client generation
    pip install openapi-python-client

    # Install dev dependencies for code formatting (optional)
    pip install black isort 2>/dev/null || true

    # Install the penpen package in development mode
    if [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
        pip install -e "$SCRIPT_DIR"
        echo "penpenパッケージをインストールしました"
    fi

    echo "Dependencies installed successfully"
}

# Generate client from OpenAPI spec
generate_client() {
    if [ "$SKIP_CLIENT" = true ]; then
        echo ""
        echo "Skipping client generation (--skip-client)"
        return
    fi

    echo ""
    echo "Downloading OpenAPI spec from $API_URL..."

    OPENAPI_FILE="$SCRIPT_DIR/openapi.yaml"
    CLIENT_DIR="$SCRIPT_DIR/generated_client"

    # Try to download OpenAPI spec
    if curl -sf "$API_URL/openapi.yaml" -o "$OPENAPI_FILE" 2>/dev/null; then
        echo "Downloaded OpenAPI spec to $OPENAPI_FILE"
    elif curl -sf "$API_URL/pao/openapi.yaml" -o "$OPENAPI_FILE" 2>/dev/null; then
        echo "Downloaded OpenAPI spec from alternate endpoint to $OPENAPI_FILE"
    else
        echo "Warning: Could not download OpenAPI spec from $API_URL"
        echo "Please run 'make download-spec API_URL=<url>' manually or ensure the API is running"
        if [ -f "$OPENAPI_FILE" ]; then
            echo "Using existing openapi.yaml file"
        else
            echo "Error: No OpenAPI spec available"
            return 1
        fi
    fi

    # Generate client if openapi file exists
    if [ -f "$OPENAPI_FILE" ]; then
        echo ""
        echo "Generating Python client..."
        if command -v openapi-python-client &> /dev/null; then
            openapi-python-client generate --path "$OPENAPI_FILE" --output-path "$CLIENT_DIR" --overwrite
            echo "Client generated in $CLIENT_DIR/"
        else
            echo "Generating client using module..."
            python -m openapi_python_client generate --path "$OPENAPI_FILE" --output-path "$CLIENT_DIR" --overwrite
            echo "Client generated in $CLIENT_DIR/"
        fi
    fi
}

# Main execution
main() {
    check_python
    check_sqlite3
    setup_venv
    install_deps
    generate_client

    echo ""
    echo "=== Installation Complete ==="
    echo ""
    echo "To activate the virtual environment, run:"
    echo "  source .venv/bin/activate"
    echo ""
    echo "To run the example:"
    echo "  python main.py"
    echo ""
}

main
#!/bin/bash
# penpenインストールスクリプト
# Usage: curl -sSL http://localhost:8080/install.sh | bash
#   or: INSTALL_SERVER=http://example.com ./install.sh

set -e

# 設定
INSTALL_SERVER="${INSTALL_SERVER:-http://localhost:10000}"
INSTALL_BASE="${INSTALL_BASE:-$HOME/.local}"
INSTALL_DIR="${INSTALL_DIR:-$INSTALL_BASE/share/penpen}"

echo "=== penpen Installer ==="
echo "Install Server: $INSTALL_SERVER"
echo "Install Directory: $INSTALL_DIR"
echo ""

# インストールサーバーのチェック
check_server() {
    echo "Checking install server..."
    if curl -sf "$INSTALL_SERVER/health" > /dev/null 2>&1; then
        echo "Install server is available"
        return 0
    else
        echo "Error: Install server not responding at $INSTALL_SERVER"
        echo "Make sure the install-server container is running:"
        echo "  docker-compose up -d install-server"
        exit 1
    fi
}

# ディレクトリ構造作成
create_directories() {
    echo ""
    echo "Creating directory structure..."
    mkdir -p "$INSTALL_DIR/src/penpen"
    mkdir -p "$INSTALL_BASE/bin"
    mkdir -p "$INSTALL_BASE/share/penpen/.venv"
    echo "  Created $INSTALL_DIR/src/penpen"
    echo "  Created $INSTALL_BASE/bin"
}

# ファイルをダウンロード
download_files() {
    echo ""
    echo "Downloading files from install server..."

    # pyproject.toml
    curl -sf "$INSTALL_SERVER/files/pyproject.toml" -o "$INSTALL_DIR/pyproject.toml"
    echo "  Downloaded pyproject.toml"

    # requirements.txt
    curl -sf "$INSTALL_SERVER/files/requirements.txt" -o "$INSTALL_DIR/requirements.txt"
    echo "  Downloaded requirements.txt"

    # Source files
    mkdir -p "$INSTALL_DIR/src/penpen"
    for file in __init__.py __main__.py cli.py executor.py prompts.py schema.sql; do
        curl -sf "$INSTALL_SERVER/files/src/penpen/$file" -o "$INSTALL_DIR/src/penpen/$file"
        echo "  Downloaded src/penpen/$file"
    done
}

# Pythonチェック
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

    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
        echo "Error: Python 3.10 or higher is required"
        exit 1
    fi
}

# SQLiteチェック
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
}

# 仮想環境作成
setup_venv() {
    echo ""
    echo "Setting up virtual environment..."

    VENV_DIR="$INSTALL_DIR/.venv"

    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        echo "  Activated existing virtual environment"
    else
        $PYTHON_CMD -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        echo "  Created virtual environment"
    fi
}

# 依存関係インストール
install_deps() {
    echo ""
    echo "Installing dependencies..."
    pip install --upgrade pip

    if [ -f "$INSTALL_DIR/requirements.txt" ]; then
        pip install -r "$INSTALL_DIR/requirements.txt"
    fi

    if [ -f "$INSTALL_DIR/pyproject.toml" ]; then
        pip install -e "$INSTALL_DIR"
        echo "penpenパッケージをインストールしました"
    fi

    echo "Dependencies installed successfully"
}

# 実行可能ファイルへのリンク作成
create_bin_link() {
    echo ""
    echo "Creating executable link..."

    PENPEN_BIN="$VENV_DIR/bin/penpen"
    LINK_PATH="$INSTALL_BASE/bin/penpen"

    if [ -f "$PENPEN_BIN" ]; then
        ln -sf "$PENPEN_BIN" "$LINK_PATH"
        echo "  Created symlink: $LINK_PATH -> $PENPEN_BIN"
    else
        echo "  Warning: penpen executable not found in venv"
    fi
}

# メイン
main() {
    check_server
    create_directories
    download_files
    check_python
    check_sqlite3
    setup_venv
    install_deps
    create_bin_link

    echo ""
    echo "=== Installation Complete ==="
    echo ""
    echo "Executable installed to: $INSTALL_BASE/bin/penpen"
    echo ""
    echo "Make sure $INSTALL_BASE/bin is in your PATH:"
    echo "  export PATH=\"$INSTALL_BASE/bin:\$PATH\""
    echo ""
    echo "Add to your shell profile (~/.bashrc or ~/.zshrc):"
    echo "  export PATH=\"$INSTALL_BASE/bin:\$PATH\""
    echo ""
    echo "--- Usage ---"
    "$VENV_DIR/bin/penpen" --help
    echo ""
}

main
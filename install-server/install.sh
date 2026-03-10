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
    mkdir -p "$INSTALL_BASE/bin"
    echo "  Created $INSTALL_BASE/bin"
}

# バイナリダウンロード
download_binary() {
    echo ""
    echo "Downloading penpen binary..."

    PENPEN_BIN="$INSTALL_BASE/bin/penpen"
    curl -sf "$INSTALL_SERVER/files/penpen" -o "$PENPEN_BIN"
    echo "  Downloaded penpen binary to $PENPEN_BIN"
}

# PATHを.bashrcに追加
setup_path() {
    echo ""
    echo "Setting up PATH..."

    # INSTALL_BASEを展開（~を実際のパスに変換）
    INSTALL_BASE_EXPANDED=$(eval echo "$INSTALL_BASE")
    PATH_LINE="export PATH=\"$INSTALL_BASE_EXPANDED/bin:\$PATH\""

    # シェル設定ファイルを決定
    if [ -n "$ZSH_VERSION" ]; then
        RC_FILE="$HOME/.zshrc"
    else
        RC_FILE="$HOME/.bashrc"
    fi

    # ファイルが存在しない場合は作成
    touch "$RC_FILE"

    # 既にPATHが追加されているか確認
    if grep -qF "$INSTALL_BASE_EXPANDED/bin" "$RC_FILE" 2>/dev/null; then
        echo "  PATH already configured in $RC_FILE"
        return 0
    fi

    # PATHを追加
    echo "" >> "$RC_FILE"
    echo "# Added by penpen installer" >> "$RC_FILE"
    echo "$PATH_LINE" >> "$RC_FILE"
    echo "  Added PATH to $RC_FILE"
    echo "  $PATH_LINE"
}

# 実行権限付与
set_permissions() {
    echo ""
    echo "Setting executable permissions..."
    chmod +x "$INSTALL_BASE/bin/penpen"
    echo "  Set executable permission on $INSTALL_BASE/bin/penpen"
}

# メイン
main() {
    check_server
    create_directories
    download_binary
    set_permissions
    setup_path

    echo ""
    echo "=== Installation Complete ==="
    echo ""
    echo "Executable installed to: $INSTALL_BASE/bin/penpen"
    echo ""
    echo "--- Usage ---"
    "$INSTALL_BASE/bin/penpen" --help
    echo ""
    echo "Restart your shell or run: source $RC_FILE"
    echo ""
}

main
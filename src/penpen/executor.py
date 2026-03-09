"""
Claude Code実行モジュール
"""

import os
import subprocess


def run_claude_command(message: str) -> int:
    """Claude Codeでプロンプトを実行

    Args:
        message: 実行するプロンプト

    Returns:
        終了コード (0: 成功, 1: エラー)
    """
    env = os.environ.copy()
    env["ANTHROPIC_AUTH_TOKEN"] = "ollama"
    env["ANTHROPIC_API_KEY"] = ""
    env["ANTHROPIC_BASE_URL"] = "http://localhost:11434"
    env["OLLAMA_CONTEXT_LENGTH"] = "65536"

    cmd = [
        "claude",
        "--model", "glm-5:cloud",
        "--output-format", "stream-json",
        "--verbose",
        "--include-partial-messages",
        "--allowedTools", "Read,Edit,Bash",
        "-p", message
    ]

    print("=== Claude Code 実行 ===\n")
    print(f"メッセージ: {message}\n")

    try:
        result = subprocess.run(cmd, env=env, check=True)
        print(f"\n終了コード: {result.returncode}")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\nエラー: {e}")
        return 1
    except FileNotFoundError:
        print("エラー: claudeコマンドが見つかりません")
        return 1
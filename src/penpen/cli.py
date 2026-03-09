"""
penpen CLI - APIクライアントツール
"""

import argparse
import os
import subprocess

from penpen.generated_client.todo_public_api_client import Client
from penpen.generated_client.todo_public_api_client.models import TodoCreate, TodoCreateStatus, TodoCreatePriority

from penpen.generated_client.todo_public_api_client.api.todos.list_todos import sync_detailed as list_todos
from penpen.generated_client.todo_public_api_client.api.todos.create_todo import sync_detailed as create_todo

API_BASE_URL = os.environ.get("API_BASE_URL", "http://172.17.0.1:10000")


def sync_example():
    """同期クライアントの使用例"""
    print("=== 同期クライアントの例 ===\n")

    with Client(base_url=API_BASE_URL) as client:
        # TODO一覧を取得
        print("TODO一覧を取得...")
        response = list_todos(client=client)
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            for todo in response.parsed:
                print(f"  - ID: {todo.id}, Title: {todo.title}, Status: {todo.status}")
        else:
            print("TODOが見つかりません")

        print()

        # 新しいTODOを作成
        print("新しいTODOを作成...")
        new_todo = TodoCreate(
            title="penpenコマンドテスト",
            description="penpenコマンドから作成したTODO",
            status=TodoCreateStatus.TODO,
            priority=TodoCreatePriority.HIGH
        )
        response = create_todo(client=client, body=new_todo)
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"作成されたTODO: ID={response.parsed.id}, Title={response.parsed.title}")


def run_claude_command(message):
    """Claude Codeでコミットを実行"""
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


    print("=== Claude Code コミット実行 ===\n")
    print(f"コマンド: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, env=env, check=True)
        print(f"\n終了コード: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"\nエラー: {e}")
    except FileNotFoundError:
        print("エラー: claudeコマンドが見つかりません")


def main():
    parser = argparse.ArgumentParser(
        prog="penpen",
        description="APIクライアントツール",
        epilog="環境変数: API_BASE_URL - APIのベースURL (デフォルト: http://localhost:10000)"
    )
    parser.parse_args()

    sync_example()
    # Claude Codeでコミット実行
    run_claude_command("適度な粒度でコミットして　メッセージは日本語で　必要に応じて、.gitignoreを追加して")


if __name__ == "__main__":
    main()
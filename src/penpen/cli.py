"""
penpen CLI - APIクライアントツール
"""

import argparse
import os
import sqlite3
from pathlib import Path

import setproctitle

from penpen.executor import run_claude_command
from penpen.prompts import prompt_commit, prompt_todo, prompt_task, prompt_run

# プロセス名を設定
setproctitle.setproctitle("penpen")

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.getcwd(), "penpen.db"))
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_incomplete_subtasks_count(db_path=None):
    """statusがcompletedではないtodo_subtasksの数を取得"""
    db_path = db_path or DB_PATH
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM todo_subtasks WHERE status != 'completed'"
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")
        return -1


def cmd_commit(args):
    """Claude Codeでコミットを実行"""
    prompt = prompt_commit()
    return run_claude_command(prompt)


def cmd_db_init(args):
    """スキーマファイルからデータベースを初期化"""
    db_path = Path(args.db_path)
    schema_path = Path(args.schema_path) if args.schema_path else SCHEMA_PATH

    if not schema_path.exists():
        print(f"エラー: スキーマファイルが見つかりません: {schema_path}")
        return 1

    db_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        conn = sqlite3.connect(db_path)
        conn.executescript(schema_sql)
        conn.close()

        print(f"データベースを初期化しました: {db_path}")
        print(f"スキーマ: {schema_path}")
        return 0
    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")
        return 1


def cmd_todo(args):
    """Claude CodeでTODOを作成"""
    prompt = prompt_todo(args.message)
    return run_claude_command(prompt)


def cmd_task(args):
    """Claude Codeでタスクを分解してサブタスクを作成"""
    prompt = prompt_task(args.message)
    return run_claude_command(prompt)


def cmd_run(args):
    """サブタスクを実行"""
    count = get_incomplete_subtasks_count()
    for i in range(count):
        prompt = prompt_run()
        return run_claude_command(prompt)


def main():
    parser = argparse.ArgumentParser(
        prog="penpen",
        usage="penpen {commit,db-init,todo,task,run} ... [-h]",
        description="Claude Code を使用したタスク管理・実行ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  penpen todo -m "バックエンドAPIの実装"    TODOを作成
  penpen task -m "フロントエンドの実装"     タスクを分解してサブタスク作成
  penpen run                               サブタスクを実行
  penpen commit                            コミットを実行
  penpen db-init                           データベースを初期化

環境変数:
  DB_PATH         データベースファイルのパス (デフォルト: /workspace/penpen.db)
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="利用可能なコマンド", metavar="COMMAND")

    # commit サブコマンド
    commit_parser = subparsers.add_parser("commit", help="Claude Codeでコミットを実行")
    commit_parser.set_defaults(func=cmd_commit)

    # db-init サブコマンド
    db_init_parser = subparsers.add_parser("db-init", help="スキーマからデータベースを初期化")
    db_init_parser.add_argument("--db-path", default=DB_PATH, help=f"データベースファイルのパス (デフォルト: {DB_PATH})")
    db_init_parser.add_argument("--schema-path", help=f"スキーマファイルのパス (デフォルト: {SCHEMA_PATH})")
    db_init_parser.set_defaults(func=cmd_db_init)

    # todo サブコマンド
    todo_parser = subparsers.add_parser("todo", help="Claude CodeでTODOを作成", description="指定した内容のTODOを作成し、データベースに保存します")
    todo_parser.add_argument("-m", "--message", required=True, help="TODOの内容")
    todo_parser.set_defaults(func=cmd_todo)

    # task サブコマンド
    task_parser = subparsers.add_parser("task", help="Claude Codeでタスクを分解してサブタスクを作成", description="タスクを分解し、todo_subtasksテーブルに保存します")
    task_parser.add_argument("-m", "--message", required=True, help="タスクの内容")
    task_parser.set_defaults(func=cmd_task)

    # run サブコマンド
    run_parser = subparsers.add_parser("run", help="サブタスクを実行", description="todo_subtasksから未完了のタスクを順に実行します")
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    main()
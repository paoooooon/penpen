"""
プロンプト生成モジュール
"""

import os

DB_PATH = os.environ.get("DB_PATH", "/workspace/penpen.db")


def prompt_commit() -> str:
    """コミット用プロンプトを生成"""
    return """適度な粒度でコミットして　メッセージは日本語で　必要に応じて、.gitignoreを追加して"""


def prompt_todo(message: str) -> str:
    """TODO作成用プロンプトを生成"""
    return f"""{message}
実装するにあたって、どんな作業が必要か、{DB_PATH}のtodosテーブルに保存してください。
これはあなた以外の人が見るので別の人が見返してわかるように客観的にお願いします
todo_subtasksの作成は不要です。 todosテーブルに詳しく書いてください"""


def prompt_task(message: str) -> str:
    """タスク分解用プロンプトを生成"""
    return f"""{message}
{DB_PATH}のtodosテーブルを実装するにあたって、どんな作業が必要か、
{DB_PATH}のtodo_subtasksテーブルに保存してください。
これはあなた以外の人が見るので別の人が見返してわかるように客観的にお願いします"""


def prompt_run() -> str:
    """サブタスク実行用プロンプトを生成"""
    return f"""{DB_PATH}のtodo_subtasksテーブルの中から、優先度の高いものを1つ選んで、実装してください。実装が終わったらステータスの更新をしてください
仕様でわからないところがあったら、仮説を立てて実装してください。どのような疑問で、どのような対応をしたのか、questionsテーブルに追加してください。
実装に関して、コマンドで生成すべきファイルを直接編集しないこと"""
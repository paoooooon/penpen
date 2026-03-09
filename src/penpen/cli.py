"""
penpen CLI - APIクライアントツール
"""

import argparse
import asyncio
import os

from .generated_client.todo_public_api_client import Client
from .generated_client.todo_public_api_client.models import TodoCreate

from .generated_client.todo_public_api_client.api.todos.list_todos import asyncio_detailed as list_todos
from .generated_client.todo_public_api_client.api.todos.create_todo import asyncio_detailed as create_todo

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:10000")


async def async_example():
    """非同期クライアントの使用例"""
    print("=== 非同期クライアントの例 ===\n")

    async with Client(base_url=API_BASE_URL) as client:
        # TODO一覧を取得
        print("TODO一覧を取得...")
        response = await list_todos(client=client)
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
            worker_id=1,
            title="penpenコマンドテスト",
            description="penpenコマンドから作成したTODO",
            status="pending",
            priority="high"
        )
        response = await create_todo(client=client, body=new_todo)
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"作成されたTODO: ID={response.parsed.id}, Title={response.parsed.title}")


def main():
    parser = argparse.ArgumentParser(
        prog="penpen",
        description="APIクライアントツール",
        epilog="環境変数: API_BASE_URL - APIのベースURL (デフォルト: http://localhost:10000)"
    )
    parser.parse_args()

    print("penpen - APIクライアントツール\n")
    print(f"API URL: {API_BASE_URL}\n")

    try:
        asyncio.run(async_example())
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    main()
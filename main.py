"""
APIクライアント使用例

生成されたOpenAPIクライアントを使用してAPIを呼び出すサンプルコード
"""

import asyncio
import os

from src.penpen.generated_client.todo_public_api_client import Client
from src.penpen.generated_client.todo_public_api_client.models import TodoCreate

# APIエンドポイント関数
from src.penpen.generated_client.todo_public_api_client.api.todos import (
    list_todos,
    create_todo,
    get_todo,
    update_todo,
)

# APIのベースURL
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:10000")


async def async_example():
    """非同期クライアントの使用例"""
    print("=== 非同期クライアントの例 ===\n")

    async with Client(base_url=API_BASE_URL) as client:
        # TODO一覧を取得
        print("TODO一覧を取得...")
        response = await list_todos.asyncio_detailed(client=client)
        if response.parsed:
            print(f"ステータスコード: {response.status_code}")
            for todo in response.parsed:
                print(f"  - ID: {todo.id}, Title: {todo.title}, Status: {todo.status}")
        else:
            print("TODOが見つかりません")

        print()

        # 新しいTODOを作成
        print("新しいTODOを作成...")
        new_todo = TodoCreate(
            title="非同期APIクライアントテスト",
            description="非同期クライアントから作成したTODO",
            status="pending",
            priority="high"
        )
        response = await create_todo.asyncio_detailed(
            client=client,
            body=new_todo
        )
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"作成されたTODO: ID={response.parsed.id}, Title={response.parsed.title}")


def main():
    print("Todoループ\n")
    print(f"API URL: {API_BASE_URL}\n")

    # 非同期クライアントの例
    try:
        asyncio.run(async_example())
    except Exception as e:
        print(f"非同期クライアントエラー: {e}")


if __name__ == "__main__":
    main()
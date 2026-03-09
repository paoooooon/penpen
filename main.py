"""
APIクライアント使用例

生成されたOpenAPIクライアントを使用してAPIを呼び出すサンプルコード
"""

import asyncio
import os
import sys

# generated_client をパスに追加
sys.path.insert(0, './generated_client')

from generated_client.my_api_client import Client
from generated_client.my_api_client.models import ProjectCreate, TodoCreate

# APIエンドポイント関数
from generated_client.my_api_client.api.todos import (
    list_todos_todos_get,
    create_todo_todos_post,
    get_todo_todos_todo_id_get,
    update_todo_todos_todo_id_put,
)
from generated_client.my_api_client.api.projects import (
    list_projects_projects_get,
    create_project_projects_post,
    get_project_projects_project_id_get,
    update_project_projects_project_id_put,
    delete_project_projects_project_id_delete,
)
from generated_client.my_api_client.api.health import get_health_health_get
from generated_client.my_api_client.api.current_project import (
    get_current_project_current_project_get,
    set_current_project_current_project_put,
    clear_current_project_current_project_delete,
)

# APIのベースURL
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:10000")


def sync_example():
    """同期クライアントの使用例"""
    print("=== 同期クライアントの例 ===\n")

    with Client(base_url=API_BASE_URL) as client:
        # ヘルスチェック
        print("ヘルスチェック...")
        response = get_health_health_get.sync_detailed(client=client)
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"  Status: {response.parsed.status}")

        print()

        # プロジェクト一覧を取得
        print("プロジェクト一覧を取得...")
        response = list_projects_projects_get.sync_detailed(client=client)
        if response.parsed:
            print(f"ステータスコード: {response.status_code}")
            for project in response.parsed:
                print(f"  - ID: {project.id}, Name: {project.name}")
        else:
            print("プロジェクトが見つかりません")

        print()

        # TODO一覧を取得
        print("TODO一覧を取得...")
        response = list_todos_todos_get.sync_detailed(client=client)
        if response.parsed:
            print(f"ステータスコード: {response.status_code}")
            for todo in response.parsed:
                print(f"  - ID: {todo.id}, Title: {todo.title}, Status: {todo.status}")
        else:
            print("TODOが見つかりません")

        print()

        # 新しいプロジェクトを作成
        print("新しいプロジェクトを作成...")
        new_project = ProjectCreate(
            name="テストプロジェクト",
            description="APIクライアントから作成したプロジェクト"
        )
        response = create_project_projects_post.sync_detailed(
            client=client,
            body=new_project
        )
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"作成されたプロジェクト: ID={response.parsed.id}, Name={response.parsed.name}")

        print()

        # 新しいTODOを作成
        print("新しいTODOを作成...")
        new_todo = TodoCreate(
            worker_id=1,
            title="APIクライアントテスト",
            description="生成されたクライアントから作成したTODO",
            status="pending",
            priority="medium"
        )
        response = create_todo_todos_post.sync_detailed(
            client=client,
            body=new_todo
        )
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"作成されたTODO: ID={response.parsed.id}, Title={response.parsed.title}")


async def async_example():
    """非同期クライアントの使用例"""
    print("=== 非同期クライアントの例 ===\n")

    async with Client(base_url=API_BASE_URL) as client:
        # ヘルスチェック
        print("ヘルスチェック...")
        response = await get_health_health_get.asyncio_detailed(client=client)
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"  Status: {response.parsed.status}")

        print()

        # プロジェクト一覧を取得
        print("プロジェクト一覧を取得...")
        response = await list_projects_projects_get.asyncio_detailed(client=client)
        if response.parsed:
            print(f"ステータスコード: {response.status_code}")
            for project in response.parsed:
                print(f"  - ID: {project.id}, Name: {project.name}")
        else:
            print("プロジェクトが見つかりません")

        print()

        # TODO一覧を取得
        print("TODO一覧を取得...")
        response = await list_todos_todos_get.asyncio_detailed(client=client)
        if response.parsed:
            print(f"ステータスコード: {response.status_code}")
            for todo in response.parsed:
                print(f"  - ID: {todo.id}, Title: {todo.title}, Status: {todo.status}")
        else:
            print("TODOが見つかりません")

        print()

        # 新しいプロジェクトを作成
        print("新しいプロジェクトを作成...")
        new_project = ProjectCreate(
            name="非同期テストプロジェクト",
            description="非同期APIクライアントから作成したプロジェクト"
        )
        response = await create_project_projects_post.asyncio_detailed(
            client=client,
            body=new_project
        )
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"作成されたプロジェクト: ID={response.parsed.id}, Name={response.parsed.name}")

        print()

        # 新しいTODOを作成
        print("新しいTODOを作成...")
        new_todo = TodoCreate(
            worker_id=1,
            title="非同期APIクライアントテスト",
            description="非同期クライアントから作成したTODO",
            status="pending",
            priority="high"
        )
        response = await create_todo_todos_post.asyncio_detailed(
            client=client,
            body=new_todo
        )
        print(f"ステータスコード: {response.status_code}")
        if response.parsed:
            print(f"作成されたTODO: ID={response.parsed.id}, Title={response.parsed.title}")


async def concurrent_requests_example():
    """複数のリクエストを並列実行する例"""
    print("=== 並列リクエストの例 ===\n")

    async with Client(base_url=API_BASE_URL) as client:
        # 複数のリクエストを並列で実行
        print("プロジェクトとTODOを並列取得...")
        projects_task = list_projects_projects_get.asyncio_detailed(client=client)
        todos_task = list_todos_todos_get.asyncio_detailed(client=client)

        # 並列実行
        projects_response, todos_response = await asyncio.gather(
            projects_task, todos_task
        )

        print("プロジェクト一覧:")
        if projects_response.parsed:
            for project in projects_response.parsed:
                print(f"  - {project.name}")

        print("\nTODO一覧:")
        if todos_response.parsed:
            for todo in todos_response.parsed:
                print(f"  - {todo.title}")


def main():
    print("APIクライアント使用例\n")
    print(f"API URL: {API_BASE_URL}\n")

    # 同期クライアントの例
    try:
        sync_example()
    except Exception as e:
        print(f"同期クライアントエラー: {e}")

    print("\n" + "=" * 50 + "\n")

    # 非同期クライアントの例
    try:
        asyncio.run(async_example())
    except Exception as e:
        print(f"非同期クライアントエラー: {e}")

    print("\n" + "=" * 50 + "\n")

    # 並列リクエストの例
    try:
        asyncio.run(concurrent_requests_example())
    except Exception as e:
        print(f"並列リクエストエラー: {e}")


if __name__ == "__main__":
    main()
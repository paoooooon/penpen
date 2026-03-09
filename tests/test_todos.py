"""
TODO APIのテスト
"""

import pytest
import respx
from httpx import Response

from my_api_client import Client
from my_api_client.api.todos import (
    list_todos_todos_get,
    create_todo_todos_post,
    get_todo_todos_todo_id_get,
    update_todo_todos_todo_id_put,
)
from my_api_client.api.todo_subtasks import (
    list_todo_subtasks_todo_subtasks_get,
    create_todo_subtask_todo_subtasks_post,
)
from my_api_client.models import TodoCreate, TodoUpdate, TodoSubtaskCreate


class TestListTodos:
    """TODO一覧取得のテスト"""

    def test_list_todos_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_todo_response: dict
    ):
        """TODO一覧取得が成功する場合"""
        respx_mock.get("http://test-api/todos").mock(
            return_value=Response(200, json=[sample_todo_response])
        )

        response = list_todos_todos_get.sync_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert len(response.parsed) == 1
        assert response.parsed[0].title == "テストTODO"

    @pytest.mark.asyncio
    async def test_list_todos_async(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_todo_response: dict
    ):
        """非同期でTODO一覧取得が成功する場合"""
        respx_mock.get("http://test-api/todos").mock(
            return_value=Response(200, json=[sample_todo_response])
        )

        response = await list_todos_todos_get.asyncio_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert len(response.parsed) == 1

    def test_list_todos_empty(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """TODOが存在しない場合"""
        respx_mock.get("http://test-api/todos").mock(
            return_value=Response(200, json=[])
        )

        response = list_todos_todos_get.sync_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert len(response.parsed) == 0


class TestCreateTodo:
    """TODO作成のテスト"""

    def test_create_todo_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_todo_response: dict
    ):
        """TODO作成が成功する場合"""
        respx_mock.post("http://test-api/todos").mock(
            return_value=Response(201, json=sample_todo_response)
        )

        new_todo = TodoCreate(
            worker_id=1,
            title="テストTODO",
            description="テスト用のTODOです",
            status="pending",
            priority="medium"
        )
        response = create_todo_todos_post.sync_detailed(
            client=client,
            body=new_todo
        )

        assert response.status_code == 201
        assert response.parsed is not None
        assert response.parsed.title == "テストTODO"
        assert response.parsed.status == "pending"

    @pytest.mark.asyncio
    async def test_create_todo_minimal_fields(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_todo_response: dict
    ):
        """最小フィールドでTODO作成が成功する場合"""
        respx_mock.post("http://test-api/todos").mock(
            return_value=Response(201, json=sample_todo_response)
        )

        new_todo = TodoCreate(worker_id=1, title="最小TODO")
        response = await create_todo_todos_post.asyncio_detailed(
            client=client,
            body=new_todo
        )

        assert response.status_code == 201
        assert response.parsed is not None

    def test_create_todo_validation_error(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """バリデーションエラーの場合"""
        respx_mock.post("http://test-api/todos").mock(
            return_value=Response(422, json={
                "detail": [
                    {
                        "loc": ["body", "title"],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            })
        )

        new_todo = TodoCreate(worker_id=1, title="")  # 空のタイトル
        response = create_todo_todos_post.sync_detailed(
            client=client,
            body=new_todo
        )

        assert response.status_code == 422


class TestGetTodo:
    """TODO取得のテスト"""

    def test_get_todo_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_todo_response: dict
    ):
        """TODO取得が成功する場合"""
        respx_mock.get("http://test-api/todos/1").mock(
            return_value=Response(200, json=sample_todo_response)
        )

        response = get_todo_todos_todo_id_get.sync_detailed(
            client=client,
            todo_id=1
        )

        assert response.status_code == 200
        assert response.parsed is not None
        assert response.parsed.id == 1

    def test_get_todo_not_found(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """TODOが見つからない場合"""
        respx_mock.get("http://test-api/todos/999").mock(
            return_value=Response(404, json={"detail": "Todo not found"})
        )

        response = get_todo_todos_todo_id_get.sync_detailed(
            client=client,
            todo_id=999
        )

        assert response.status_code == 404


class TestUpdateTodo:
    """TODO更新のテスト"""

    def test_update_todo_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_todo_response: dict
    ):
        """TODO更新が成功する場合"""
        updated_response = sample_todo_response.copy()
        updated_response["status"] = "completed"

        respx_mock.put("http://test-api/todos/1").mock(
            return_value=Response(200, json=updated_response)
        )

        update_data = TodoUpdate(status="completed")
        response = update_todo_todos_todo_id_put.sync_detailed(
            client=client,
            todo_id=1,
            body=update_data
        )

        assert response.status_code == 200
        assert response.parsed is not None
        assert response.parsed.status == "completed"

    @pytest.mark.asyncio
    async def test_update_todo_async(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_todo_response: dict
    ):
        """非同期でTODO更新が成功する場合"""
        updated_response = sample_todo_response.copy()
        updated_response["priority"] = "high"

        respx_mock.put("http://test-api/todos/1").mock(
            return_value=Response(200, json=updated_response)
        )

        update_data = TodoUpdate(priority="high")
        response = await update_todo_todos_todo_id_put.asyncio_detailed(
            client=client,
            todo_id=1,
            body=update_data
        )

        assert response.status_code == 200
        assert response.parsed is not None


class TestTodoSubtasks:
    """TODOサブタスクのテスト"""

    def test_list_subtasks(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """サブタスク一覧取得が成功する場合"""
        subtask_response = {
            "id": 1,
            "todo_id": 1,
            "title": "サブタスク1",
            "status": "pending",
            "sort_order": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        respx_mock.get("http://test-api/todo-subtasks").mock(
            return_value=Response(200, json=[subtask_response])
        )

        response = list_todo_subtasks_todo_subtasks_get.sync_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert len(response.parsed) == 1

    def test_create_subtask(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """サブタスク作成が成功する場合"""
        subtask_response = {
            "id": 1,
            "todo_id": 1,
            "title": "新しいサブタスク",
            "status": "pending",
            "sort_order": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        respx_mock.post("http://test-api/todo-subtasks").mock(
            return_value=Response(201, json=subtask_response)
        )

        new_subtask = TodoSubtaskCreate(todo_id=1, title="新しいサブタスク")
        response = create_todo_subtask_todo_subtasks_post.sync_detailed(
            client=client,
            body=new_subtask
        )

        assert response.status_code == 201
        assert response.parsed is not None
        assert response.parsed.title == "新しいサブタスク"
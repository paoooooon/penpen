"""
テスト用の共通フィクスチャ
"""

import pytest
import respx
from my_api_client import Client


@pytest.fixture
def api_base_url() -> str:
    """APIのベースURL"""
    return "http://test-api"


@pytest.fixture
def client(api_base_url: str) -> Client:
    """同期クライアントのフィクスチャ"""
    return Client(base_url=api_base_url)


@pytest.fixture
def respx_mock():
    """HTTPリクエストをモックするフィクスチャ"""
    with respx.mock(assert_all_called=False) as mock:
        yield mock


@pytest.fixture
def sample_project_response() -> dict:
    """サンプルのプロジェクトレスポンス"""
    return {
        "id": 1,
        "name": "テストプロジェクト",
        "description": "テスト用のプロジェクトです",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def sample_todo_response() -> dict:
    """サンプルのTODOレスポンス"""
    return {
        "id": 1,
        "project_id": 1,
        "worker_id": 1,
        "agent_id": None,
        "title": "テストTODO",
        "description": "テスト用のTODOです",
        "status": "pending",
        "priority": "medium",
        "due_date": None,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def sample_health_response() -> dict:
    """サンプルのヘルスチェックレスポンス"""
    return {"status": "healthy"}
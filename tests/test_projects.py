"""
プロジェクトAPIのテスト
"""

import pytest
import respx
from httpx import Response

from my_api_client import Client
from my_api_client.api.projects import (
    list_projects_projects_get,
    create_project_projects_post,
    get_project_projects_project_id_get,
    update_project_projects_project_id_put,
    delete_project_projects_project_id_delete,
)
from my_api_client.models import ProjectCreate, ProjectUpdate, Project


class TestListProjects:
    """プロジェクト一覧取得のテスト"""

    def test_list_projects_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_project_response: dict
    ):
        """プロジェクト一覧取得が成功する場合"""
        # モックの設定
        respx_mock.get("http://test-api/projects").mock(
            return_value=Response(200, json=[sample_project_response])
        )

        # テスト実行
        response = list_projects_projects_get.sync_detailed(client=client)

        # 検証
        assert response.status_code == 200
        assert response.parsed is not None
        assert len(response.parsed) == 1
        assert response.parsed[0].name == "テストプロジェクト"

    @pytest.mark.asyncio
    async def test_list_projects_async(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_project_response: dict
    ):
        """非同期でプロジェクト一覧取得が成功する場合"""
        respx_mock.get("http://test-api/projects").mock(
            return_value=Response(200, json=[sample_project_response])
        )

        response = await list_projects_projects_get.asyncio_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert len(response.parsed) == 1

    def test_list_projects_empty(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """プロジェクトが存在しない場合"""
        respx_mock.get("http://test-api/projects").mock(
            return_value=Response(200, json=[])
        )

        response = list_projects_projects_get.sync_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert len(response.parsed) == 0


class TestCreateProject:
    """プロジェクト作成のテスト"""

    def test_create_project_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_project_response: dict
    ):
        """プロジェクト作成が成功する場合"""
        respx_mock.post("http://test-api/projects").mock(
            return_value=Response(201, json=sample_project_response)
        )

        new_project = ProjectCreate(
            name="テストプロジェクト",
            description="テスト用のプロジェクトです"
        )
        response = create_project_projects_post.sync_detailed(
            client=client,
            body=new_project
        )

        assert response.status_code == 201
        assert response.parsed is not None
        assert response.parsed.name == "テストプロジェクト"

    @pytest.mark.asyncio
    async def test_create_project_async(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_project_response: dict
    ):
        """非同期でプロジェクト作成が成功する場合"""
        respx_mock.post("http://test-api/projects").mock(
            return_value=Response(201, json=sample_project_response)
        )

        new_project = ProjectCreate(name="テストプロジェクト")
        response = await create_project_projects_post.asyncio_detailed(
            client=client,
            body=new_project
        )

        assert response.status_code == 201
        assert response.parsed is not None


class TestGetProject:
    """プロジェクト取得のテスト"""

    def test_get_project_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_project_response: dict
    ):
        """プロジェクト取得が成功する場合"""
        respx_mock.get("http://test-api/projects/1").mock(
            return_value=Response(200, json=sample_project_response)
        )

        response = get_project_projects_project_id_get.sync_detailed(
            client=client,
            project_id=1
        )

        assert response.status_code == 200
        assert response.parsed is not None
        assert response.parsed.id == 1

    def test_get_project_not_found(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """プロジェクトが見つからない場合"""
        respx_mock.get("http://test-api/projects/999").mock(
            return_value=Response(404, json={"detail": "Project not found"})
        )

        response = get_project_projects_project_id_get.sync_detailed(
            client=client,
            project_id=999
        )

        assert response.status_code == 404
        # 404の場合はErrorモデルがパースされる
        assert response.parsed is not None
        assert hasattr(response.parsed, 'detail')


class TestUpdateProject:
    """プロジェクト更新のテスト"""

    def test_update_project_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_project_response: dict
    ):
        """プロジェクト更新が成功する場合"""
        updated_response = sample_project_response.copy()
        updated_response["name"] = "更新されたプロジェクト"

        respx_mock.put("http://test-api/projects/1").mock(
            return_value=Response(200, json=updated_response)
        )

        update_data = ProjectUpdate(name="更新されたプロジェクト")
        response = update_project_projects_project_id_put.sync_detailed(
            client=client,
            project_id=1,
            body=update_data
        )

        assert response.status_code == 200
        assert response.parsed is not None
        assert response.parsed.name == "更新されたプロジェクト"


class TestDeleteProject:
    """プロジェクト削除のテスト"""

    def test_delete_project_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """プロジェクト削除が成功する場合"""
        respx_mock.delete("http://test-api/projects/1").mock(
            return_value=Response(204)
        )

        response = delete_project_projects_project_id_delete.sync_detailed(
            client=client,
            project_id=1
        )

        assert response.status_code == 204
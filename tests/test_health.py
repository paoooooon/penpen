"""
ヘルスチェックAPIのテスト
"""

import pytest
import respx
from httpx import Response

from my_api_client import Client
from my_api_client.api.health import get_health_health_get


class TestHealthCheck:
    """ヘルスチェックのテスト"""

    def test_health_check_success(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_health_response: dict
    ):
        """ヘルスチェックが成功する場合"""
        respx_mock.get("http://test-api/health").mock(
            return_value=Response(200, json=sample_health_response)
        )

        response = get_health_health_get.sync_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert response.parsed.status == "healthy"

    @pytest.mark.asyncio
    async def test_health_check_async(
        self,
        client: Client,
        respx_mock: respx.MockRouter,
        sample_health_response: dict
    ):
        """非同期でヘルスチェックが成功する場合"""
        respx_mock.get("http://test-api/health").mock(
            return_value=Response(200, json=sample_health_response)
        )

        response = await get_health_health_get.asyncio_detailed(client=client)

        assert response.status_code == 200
        assert response.parsed is not None
        assert response.parsed.status == "healthy"

    def test_health_check_service_unavailable(
        self,
        client: Client,
        respx_mock: respx.MockRouter
    ):
        """サービスが利用できない場合"""
        respx_mock.get("http://test-api/health").mock(
            return_value=Response(503, json={"status": "unhealthy"})
        )

        # raise_on_unexpected_status=True で例外を発生させる
        client_with_raise = Client(base_url="http://test-api", raise_on_unexpected_status=True)

        with pytest.raises(Exception):  # UnexpectedStatus 例外が発生するはず
            get_health_health_get.sync_detailed(client=client_with_raise)
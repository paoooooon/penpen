"""
クライアントのテスト
"""

import pytest
from my_api_client import Client, AuthenticatedClient


class TestClient:
    """Clientクラスのテスト"""

    def test_client_creation(self):
        """クライアントが正しく作成されるか"""
        client = Client(base_url="http://test-api")

        assert client._base_url == "http://test-api"
        assert client._cookies == {}
        assert client._headers == {}

    def test_client_with_headers(self):
        """ヘッダー付きでクライアントが作成されるか"""
        client = Client(
            base_url="http://test-api",
            headers={"X-Custom-Header": "test-value"}
        )

        assert client._headers == {"X-Custom-Header": "test-value"}

    def test_client_with_cookies(self):
        """クッキー付きでクライアントが作成されるか"""
        client = Client(
            base_url="http://test-api",
            cookies={"session_id": "abc123"}
        )

        assert client._cookies == {"session_id": "abc123"}

    def test_client_with_timeout(self):
        """タイムアウト設定付きでクライアントが作成されるか"""
        import httpx

        client = Client(
            base_url="http://test-api",
            timeout=httpx.Timeout(30.0)
        )

        assert client._timeout is not None

    def test_client_raise_on_unexpected_status(self):
        """raise_on_unexpected_status設定が正しく動作するか"""
        client = Client(
            base_url="http://test-api",
            raise_on_unexpected_status=True
        )

        assert client.raise_on_unexpected_status is True

    def test_client_with_headers_method(self):
        """with_headersメソッドが正しく動作するか"""
        client = Client(
            base_url="http://test-api",
            headers={"X-Initial": "value"}
        )

        new_client = client.with_headers({"X-Additional": "new-value"})

        assert "X-Initial" in new_client._headers
        assert "X-Additional" in new_client._headers


class TestAuthenticatedClient:
    """AuthenticatedClientクラスのテスト"""

    def test_authenticated_client_creation(self):
        """認証付きクライアントが正しく作成されるか"""
        client = AuthenticatedClient(
            base_url="http://test-api",
            token="test-token"
        )

        assert client._base_url == "http://test-api"
        assert client.token == "test-token"
        assert client.prefix == "Bearer"
        assert client.auth_header_name == "Authorization"

    def test_authenticated_client_custom_prefix(self):
        """カスタムプレフィックス付きでクライアントが作成されるか"""
        client = AuthenticatedClient(
            base_url="http://test-api",
            token="test-token",
            prefix="Token"
        )

        assert client.prefix == "Token"

    def test_authenticated_client_custom_header_name(self):
        """カスタムヘッダー名付きでクライアントが作成されるか"""
        client = AuthenticatedClient(
            base_url="http://test-api",
            token="test-token",
            auth_header_name="X-API-Key"
        )

        assert client.auth_header_name == "X-API-Key"
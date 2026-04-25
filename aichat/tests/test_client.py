"""Tests for the AiChat API client."""

import pytest
import respx
from httpx import Response

from aichat_cli.core.client import AichatClient, get_client
from aichat_cli.core.exceptions import AichatAPIError, AichatAuthError, AichatTimeoutError


class TestAichatClient:
    """Tests for AichatClient."""

    def test_init_with_token(self):
        client = AichatClient(api_token="test-token")
        assert client.api_token == "test-token"

    def test_init_default_base_url(self):
        client = AichatClient(api_token="test-token")
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom_base_url(self):
        client = AichatClient(api_token="test-token", base_url="https://custom.example.com")
        assert client.base_url == "https://custom.example.com"

    def test_get_headers(self):
        client = AichatClient(api_token="test-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self):
        client = AichatClient(api_token="")
        with pytest.raises(AichatAuthError):
            client._get_headers()

    @respx.mock
    def test_converse_success(self, mock_conversation_response):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        client = AichatClient(api_token="test-token")
        result = client.converse(question="Hello?", model="gpt-4o")
        assert result["answer"] is not None
        assert result["id"] is not None

    @respx.mock
    def test_converse_invalid_token(self):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(401, json={"error": {"code": "invalid_token"}})
        )
        client = AichatClient(api_token="bad-token")
        with pytest.raises(AichatAuthError):
            client.converse(question="Hello?", model="gpt-4o")

    @respx.mock
    def test_converse_api_error(self):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = AichatClient(api_token="test-token")
        with pytest.raises(AichatAPIError):
            client.converse(question="Hello?", model="gpt-4o")

    @respx.mock
    def test_none_values_excluded(self):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json={"id": "abc", "answer": "Hi"})
        )
        client = AichatClient(api_token="test-token")
        client.converse(question="Hello?", model="gpt-4o", id=None, preset=None)
        import json

        body = json.loads(route.calls.last.request.content)
        assert "id" not in body
        assert "preset" not in body


class TestGetClient:
    """Tests for the get_client factory."""

    def test_get_client_with_token(self):
        client = get_client("my-token")
        assert client.api_token == "my-token"

    def test_get_client_without_token(self):
        client = get_client()
        assert isinstance(client, AichatClient)

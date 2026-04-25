"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from aichat_cli.core.client import AichatClient
from aichat_cli.core.exceptions import (
    AichatAPIError,
    AichatAuthError,
    AichatTimeoutError,
)


class TestAichatClient:
    """Tests for AichatClient."""

    def test_init_default(self):
        client = AichatClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = AichatClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = AichatClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = AichatClient(api_token="")
        with pytest.raises(AichatAuthError):
            client._get_headers()

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(
                200,
                json={"id": "abc123", "answer": "Hello!"},
            )
        )
        client = AichatClient(api_token="test-token")
        result = client.request(
            "/aichat/conversations", {"question": "Hi", "model": "gpt-4o"}
        )
        assert result["id"] == "abc123"
        assert result["answer"] == "Hello!"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = AichatClient(api_token="bad-token")
        with pytest.raises(AichatAuthError, match="Invalid API token"):
            client.request("/aichat/conversations", {"question": "Hi", "model": "gpt-4o"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = AichatClient(api_token="test-token")
        with pytest.raises(AichatAuthError, match="Access denied"):
            client.request("/aichat/conversations", {"question": "Hi", "model": "gpt-4o"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = AichatClient(api_token="test-token")
        with pytest.raises(AichatAPIError) as exc_info:
            client.request("/aichat/conversations", {"question": "Hi", "model": "gpt-4o"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = AichatClient(api_token="test-token")
        with pytest.raises(AichatTimeoutError):
            client.request(
                "/aichat/conversations", {"question": "Hi", "model": "gpt-4o"}, timeout=1
            )

    @respx.mock
    def test_request_removes_none_values(self):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json={"id": "abc", "answer": "Hello"})
        )
        client = AichatClient(api_token="test-token")
        import json

        client.request(
            "/aichat/conversations",
            {"question": "Hi", "model": "gpt-4o", "id": None, "preset": None},
        )
        body = json.loads(route.calls.last.request.content)
        assert "id" not in body
        assert "preset" not in body

    @respx.mock
    def test_converse(self):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(
                200,
                json={"id": "abc123", "answer": "Paris"},
            )
        )
        client = AichatClient(api_token="test-token")
        result = client.converse(question="Capital of France?", model="gpt-4o")
        assert result["answer"] == "Paris"

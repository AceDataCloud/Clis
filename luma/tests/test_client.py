"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from luma_cli.core.client import LumaClient
from luma_cli.core.exceptions import (
    LumaAPIError,
    LumaAuthError,
    LumaTimeoutError,
)


class TestLumaClient:
    """Tests for LumaClient."""

    def test_init_default(self):
        client = LumaClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = LumaClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = LumaClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = LumaClient(api_token="")
        with pytest.raises(LumaAuthError):
            client._get_headers()

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(200, json={"success": True, "task_id": "t-123"})
        )
        client = LumaClient(api_token="test-token")
        result = client.request("/luma/videos", {"prompt": "test"})
        assert result["success"] is True
        assert result["task_id"] == "t-123"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = LumaClient(api_token="bad-token")
        with pytest.raises(LumaAuthError, match="Invalid API token"):
            client.request("/luma/videos", {"prompt": "test"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = LumaClient(api_token="test-token")
        with pytest.raises(LumaAuthError, match="Access denied"):
            client.request("/luma/videos", {"prompt": "test"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = LumaClient(api_token="test-token")
        with pytest.raises(LumaAPIError) as exc_info:
            client.request("/luma/videos", {"prompt": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/luma/videos").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = LumaClient(api_token="test-token")
        with pytest.raises(LumaTimeoutError):
            client.request("/luma/videos", {"prompt": "test"}, timeout=1)

    @respx.mock
    def test_request_removes_none_values(self):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(200, json={"success": True})
        )
        client = LumaClient(api_token="test-token")
        result = client.request(
            "/luma/videos",
            {"prompt": "test", "callback_url": None},
        )
        assert result["success"] is True

    @respx.mock
    def test_generate_video(self):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(200, json={"success": True, "task_id": "gen-123"})
        )
        client = LumaClient(api_token="test-token")
        result = client.generate_video(prompt="test")
        assert result["task_id"] == "gen-123"

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/luma/tasks").mock(
            return_value=Response(200, json={"success": True, "data": [{"id": "t-1"}]})
        )
        client = LumaClient(api_token="test-token")
        result = client.query_task(id="t-1", action="retrieve")
        assert result["data"][0]["id"] == "t-1"

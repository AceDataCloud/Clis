"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from seedream_cli.core.client import SeedreamClient
from seedream_cli.core.exceptions import (
    SeedreamAPIError,
    SeedreamAuthError,
    SeedreamTimeoutError,
)


class TestSeedreamClient:
    """Tests for SeedreamClient."""

    def test_init_default(self):
        client = SeedreamClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = SeedreamClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = SeedreamClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = SeedreamClient(api_token="")
        with pytest.raises(SeedreamAuthError):
            client._get_headers()

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "t-123"})
        )
        client = SeedreamClient(api_token="test-token")
        result = client.request("/seedream/images", {"prompt": "test"})
        assert result["success"] is True
        assert result["task_id"] == "t-123"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = SeedreamClient(api_token="bad-token")
        with pytest.raises(SeedreamAuthError, match="Invalid API token"):
            client.request("/seedream/images", {"prompt": "test"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = SeedreamClient(api_token="test-token")
        with pytest.raises(SeedreamAuthError, match="Access denied"):
            client.request("/seedream/images", {"prompt": "test"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = SeedreamClient(api_token="test-token")
        with pytest.raises(SeedreamAPIError) as exc_info:
            client.request("/seedream/images", {"prompt": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/seedream/images").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = SeedreamClient(api_token="test-token")
        with pytest.raises(SeedreamTimeoutError):
            client.request("/seedream/images", {"prompt": "test"}, timeout=1)

    @respx.mock
    def test_request_removes_none_values(self):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json={"success": True})
        )
        client = SeedreamClient(api_token="test-token")
        result = client.request(
            "/seedream/images",
            {"prompt": "test", "callback_url": None},
        )
        assert result["success"] is True

    @respx.mock
    def test_generate_image(self):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "gen-123"})
        )
        client = SeedreamClient(api_token="test-token")
        result = client.generate_image(prompt="test")
        assert result["task_id"] == "gen-123"

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/seedream/tasks").mock(
            return_value=Response(200, json={"success": True, "data": [{"id": "t-1"}]})
        )
        client = SeedreamClient(api_token="test-token")
        result = client.query_task(id="t-1", action="retrieve")
        assert result["data"][0]["id"] == "t-1"

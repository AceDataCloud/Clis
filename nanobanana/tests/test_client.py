"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from nanobanana_cli.core.client import NanoBananaClient
from nanobanana_cli.core.exceptions import (
    NanoBananaAPIError,
    NanoBananaAuthError,
    NanoBananaTimeoutError,
)


class TestNanoBananaClient:
    """Tests for NanoBananaClient."""

    def test_init_default(self):
        client = NanoBananaClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = NanoBananaClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = NanoBananaClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = NanoBananaClient(api_token="")
        with pytest.raises(NanoBananaAuthError):
            client._get_headers()

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "t-123"})
        )
        client = NanoBananaClient(api_token="test-token")
        result = client.request("/nano-banana/images", {"action": "generate", "prompt": "test"})
        assert result["success"] is True
        assert result["task_id"] == "t-123"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = NanoBananaClient(api_token="bad-token")
        with pytest.raises(NanoBananaAuthError, match="Invalid API token"):
            client.request("/nano-banana/images", {"action": "generate"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = NanoBananaClient(api_token="test-token")
        with pytest.raises(NanoBananaAuthError, match="Access denied"):
            client.request("/nano-banana/images", {"action": "generate"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = NanoBananaClient(api_token="test-token")
        with pytest.raises(NanoBananaAPIError) as exc_info:
            client.request("/nano-banana/images", {"action": "generate"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = NanoBananaClient(api_token="test-token")
        with pytest.raises(NanoBananaTimeoutError):
            client.request("/nano-banana/images", {"action": "generate"}, timeout=1)

    @respx.mock
    def test_request_removes_none_values(self):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json={"success": True})
        )
        client = NanoBananaClient(api_token="test-token")
        result = client.request(
            "/nano-banana/images",
            {"action": "generate", "prompt": "test", "callback_url": None},
        )
        assert result["success"] is True

    @respx.mock
    def test_generate_image(self):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "gen-123"})
        )
        client = NanoBananaClient(api_token="test-token")
        result = client.generate_image(action="generate", prompt="a cat")
        assert result["task_id"] == "gen-123"

    @respx.mock
    def test_edit_image(self):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "edit-123"})
        )
        client = NanoBananaClient(api_token="test-token")
        result = client.edit_image(
            action="edit", prompt="make it blue", image_urls=["https://example.com/img.jpg"]
        )
        assert result["task_id"] == "edit-123"

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/nano-banana/tasks").mock(
            return_value=Response(200, json={"success": True, "data": [{"id": "t-1"}]})
        )
        client = NanoBananaClient(api_token="test-token")
        result = client.query_task(id="t-1", action="retrieve")
        assert result["data"][0]["id"] == "t-1"

"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from flux_cli.core.client import FluxClient
from flux_cli.core.exceptions import (
    FluxAPIError,
    FluxAuthError,
    FluxTimeoutError,
)


class TestFluxClient:
    """Tests for FluxClient."""

    def test_init_default(self):
        client = FluxClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = FluxClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = FluxClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = FluxClient(api_token="")
        with pytest.raises(FluxAuthError):
            client._get_headers()

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "t-123"})
        )
        client = FluxClient(api_token="test-token")
        result = client.request("/flux/images", {"prompt": "test"})
        assert result["success"] is True
        assert result["task_id"] == "t-123"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = FluxClient(api_token="bad-token")
        with pytest.raises(FluxAuthError, match="Invalid API token"):
            client.request("/flux/images", {"prompt": "test"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = FluxClient(api_token="test-token")
        with pytest.raises(FluxAuthError, match="Access denied"):
            client.request("/flux/images", {"prompt": "test"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = FluxClient(api_token="test-token")
        with pytest.raises(FluxAPIError) as exc_info:
            client.request("/flux/images", {"prompt": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/flux/images").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = FluxClient(api_token="test-token")
        with pytest.raises(FluxTimeoutError):
            client.request("/flux/images", {"prompt": "test"}, timeout=1)

    @respx.mock
    def test_request_removes_none_values(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"success": True})
        )
        client = FluxClient(api_token="test-token")
        result = client.request(
            "/flux/images",
            {"prompt": "test", "callback_url": None},
        )
        assert result["success"] is True

    @respx.mock
    def test_generate_image(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "gen-123"})
        )
        client = FluxClient(api_token="test-token")
        result = client.generate_image(prompt="test")
        assert result["task_id"] == "gen-123"

    @respx.mock
    def test_edit_image(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"success": True, "task_id": "edit-123"})
        )
        client = FluxClient(api_token="test-token")
        result = client.edit_image(
            prompt="add sunglasses",
            image_url="https://example.com/photo.jpg",
        )
        assert result["task_id"] == "edit-123"

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/flux/tasks").mock(
            return_value=Response(200, json={"success": True, "data": [{"id": "t-1"}]})
        )
        client = FluxClient(api_token="test-token")
        result = client.query_task(id="t-1", action="retrieve")
        assert result["data"][0]["id"] == "t-1"

    @respx.mock
    def test_with_async_callback(self):
        route = respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"success": True})
        )
        client = FluxClient(api_token="test-token")
        client.generate_image(prompt="test")
        import json

        body = json.loads(route.calls.last.request.content)
        assert "callback_url" in body

    @respx.mock
    def test_with_async_callback_preserves_custom(self):
        route = respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"success": True})
        )
        client = FluxClient(api_token="test-token")
        client.generate_image(prompt="test", callback_url="https://my.webhook/cb")
        import json

        body = json.loads(route.calls.last.request.content)
        assert body["callback_url"] == "https://my.webhook/cb"

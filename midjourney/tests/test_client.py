"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from midjourney_cli.core.client import MidjourneyClient
from midjourney_cli.core.exceptions import (
    MidjourneyAPIError,
    MidjourneyAuthError,
    MidjourneyTimeoutError,
)


class TestMidjourneyClient:
    """Tests for MidjourneyClient."""

    def test_init_default(self):
        client = MidjourneyClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = MidjourneyClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = MidjourneyClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = MidjourneyClient(api_token="")
        with pytest.raises(MidjourneyAuthError):
            client._get_headers()

    def test_async_callback(self):
        client = MidjourneyClient(api_token="test-token")
        payload = {"prompt": "test"}
        result = client._with_async_callback(payload)
        assert "callback_url" in result
        assert result["prompt"] == "test"

    def test_async_callback_preserves_existing(self):
        client = MidjourneyClient(api_token="test-token")
        payload = {"prompt": "test", "callback_url": "https://my.callback"}
        result = client._with_async_callback(payload)
        assert result["callback_url"] == "https://my.callback"

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json={"success": True, "task_id": "t-123"})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.request("/midjourney/imagine", {"prompt": "test"})
        assert result["success"] is True
        assert result["task_id"] == "t-123"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = MidjourneyClient(api_token="bad-token")
        with pytest.raises(MidjourneyAuthError, match="Invalid API token"):
            client.request("/midjourney/imagine", {"prompt": "test"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = MidjourneyClient(api_token="test-token")
        with pytest.raises(MidjourneyAuthError, match="Access denied"):
            client.request("/midjourney/imagine", {"prompt": "test"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = MidjourneyClient(api_token="test-token")
        with pytest.raises(MidjourneyAPIError) as exc_info:
            client.request("/midjourney/imagine", {"prompt": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = MidjourneyClient(api_token="test-token")
        with pytest.raises(MidjourneyTimeoutError):
            client.request("/midjourney/imagine", {"prompt": "test"}, timeout=1)

    @respx.mock
    def test_request_removes_none_values(self):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json={"success": True})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.request(
            "/midjourney/imagine",
            {"prompt": "test", "callback_url": None},
        )
        assert result["success"] is True

    @respx.mock
    def test_imagine(self):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json={"success": True, "task_id": "img-123"})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.imagine(prompt="test", action="generate")
        assert result["task_id"] == "img-123"

    @respx.mock
    def test_describe(self):
        respx.post("https://api.acedata.cloud/midjourney/describe").mock(
            return_value=Response(200, json={"success": True, "descriptions": ["desc"]})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.describe(image_url="https://example.com/img.jpg")
        assert result["descriptions"] == ["desc"]

    @respx.mock
    def test_edit(self):
        respx.post("https://api.acedata.cloud/midjourney/edits").mock(
            return_value=Response(200, json={"success": True, "task_id": "edit-123"})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.edit(image_url="https://example.com/img.jpg", prompt="test")
        assert result["task_id"] == "edit-123"

    @respx.mock
    def test_generate_video(self):
        respx.post("https://api.acedata.cloud/midjourney/videos").mock(
            return_value=Response(200, json={"success": True, "task_id": "vid-123"})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.generate_video(prompt="test", image_url="https://example.com/img.jpg")
        assert result["task_id"] == "vid-123"

    @respx.mock
    def test_translate(self):
        respx.post("https://api.acedata.cloud/midjourney/translate").mock(
            return_value=Response(200, json={"success": True, "translated_content": "hello"})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.translate(content="你好")
        assert result["translated_content"] == "hello"

    @respx.mock
    def test_get_seed(self):
        respx.post("https://api.acedata.cloud/midjourney/seed").mock(
            return_value=Response(200, json={"success": True, "seed": 12345})
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.get_seed(image_id="img-123")
        assert result["seed"] == 12345

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(
                200, json={"success": True, "image_url": "https://example.com/result.png"}
            )
        )
        client = MidjourneyClient(api_token="test-token")
        result = client.query_task(id="t-1", action="retrieve")
        assert result["image_url"] == "https://example.com/result.png"

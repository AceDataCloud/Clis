"""Tests for HTTP client."""

import json

import pytest
import respx
from httpx import Response

from adc_cli.core.client import AdcClient, get_client
from adc_cli.core.exceptions import (
    AdcAPIError,
    AdcAuthError,
    AdcTimeoutError,
)


class TestAdcClient:
    """Tests for AdcClient."""

    def test_init_default(self):
        client = AdcClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = AdcClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = AdcClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = AdcClient(api_token="")
        with pytest.raises(AdcAuthError):
            client._get_headers()

    def test_with_async_callback(self):
        client = AdcClient(api_token="test-token")
        payload = {"prompt": "test"}
        result = client._with_async_callback(payload)
        assert result["callback_url"] == "https://api.acedata.cloud/health"
        assert result["prompt"] == "test"
        # Original should not be modified
        assert "callback_url" not in payload

    def test_with_async_callback_preserves_existing(self):
        client = AdcClient(api_token="test-token")
        payload = {"prompt": "test", "callback_url": "https://my-callback.com"}
        result = client._with_async_callback(payload)
        assert result["callback_url"] == "https://my-callback.com"

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"task_id": "abc"})
        )
        client = AdcClient(api_token="test-token")
        result = client.request("/flux/images", {"prompt": "test"})
        assert result["task_id"] == "abc"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = AdcClient(api_token="bad-token")
        with pytest.raises(AdcAuthError, match="Invalid API token"):
            client.request("/flux/images", {"prompt": "test"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = AdcClient(api_token="test-token")
        with pytest.raises(AdcAuthError, match="Access denied"):
            client.request("/flux/images", {"prompt": "test"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = AdcClient(api_token="test-token")
        with pytest.raises(AdcAPIError) as exc_info:
            client.request("/flux/images", {"prompt": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/flux/images").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = AdcClient(api_token="test-token")
        with pytest.raises(AdcTimeoutError):
            client.request("/flux/images", {"prompt": "test"}, timeout=1)

    @respx.mock
    def test_request_removes_none_values(self):
        route = respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"task_id": "abc"})
        )
        client = AdcClient(api_token="test-token")
        client.request("/flux/images", {"prompt": "test", "model": None, "size": None})
        body = json.loads(route.calls.last.request.content)
        assert "model" not in body
        assert "size" not in body
        assert body["prompt"] == "test"


class TestConvenienceMethods:
    """Tests for service-specific convenience methods."""

    @respx.mock
    def test_flux_image(self):
        route = respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json={"task_id": "flux-1"})
        )
        client = AdcClient(api_token="test-token")
        result = client.flux_image(prompt="sunset", model="flux-dev")
        assert result["task_id"] == "flux-1"
        body = json.loads(route.calls.last.request.content)
        assert body["callback_url"] == "https://api.acedata.cloud/health"

    @respx.mock
    def test_midjourney_imagine(self):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json={"task_id": "mj-1"})
        )
        client = AdcClient(api_token="test-token")
        result = client.midjourney_imagine(prompt="city")
        assert result["task_id"] == "mj-1"
        body = json.loads(route.calls.last.request.content)
        assert "callback_url" in body

    @respx.mock
    def test_suno_music(self):
        route = respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json={"task_id": "suno-1"})
        )
        client = AdcClient(api_token="test-token")
        result = client.suno_music(action="generate", prompt="jazz")
        assert result["task_id"] == "suno-1"
        body = json.loads(route.calls.last.request.content)
        assert "callback_url" in body

    @respx.mock
    def test_luma_video(self):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(200, json={"task_id": "luma-1"})
        )
        client = AdcClient(api_token="test-token")
        result = client.luma_video(prompt="ocean")
        assert result["task_id"] == "luma-1"

    @respx.mock
    def test_sora_video(self):
        respx.post("https://api.acedata.cloud/sora/videos").mock(
            return_value=Response(200, json={"task_id": "sora-1"})
        )
        client = AdcClient(api_token="test-token")
        result = client.sora_video(prompt="rocket")
        assert result["task_id"] == "sora-1"

    @respx.mock
    def test_serp_search(self):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json={"organic": []})
        )
        client = AdcClient(api_token="test-token")
        result = client.serp_search(query="test", type="search")
        assert "organic" in result
        # serp_search should NOT add callback_url
        body = json.loads(route.calls.last.request.content)
        assert "callback_url" not in body

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/flux/tasks").mock(
            return_value=Response(200, json={"data": [{"state": "succeeded"}]})
        )
        client = AdcClient(api_token="test-token")
        result = client.query_task("flux", id="task-123", action="retrieve")
        assert result["data"][0]["state"] == "succeeded"


class TestGetClient:
    """Tests for get_client factory."""

    def test_get_client_with_token(self):
        client = get_client("explicit-token")
        assert client.api_token == "explicit-token"

    def test_get_client_default(self):
        client = get_client(None)
        assert isinstance(client, AdcClient)

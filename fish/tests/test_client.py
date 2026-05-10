"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from fish_cli.core.client import FishClient
from fish_cli.core.exceptions import (
    FishAPIError,
    FishAuthError,
    FishTimeoutError,
)


class TestFishClient:
    """Tests for FishClient."""

    def test_init_default(self):
        client = FishClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = FishClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = FishClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = FishClient(api_token="")
        with pytest.raises(FishAuthError):
            client._get_headers()

    def test_headers_with_extra(self):
        client = FishClient(api_token="my-token")
        headers = client._get_headers(extra={"model": "s1"})
        assert headers["model"] == "s1"
        assert headers["authorization"] == "Bearer my-token"

    @respx.mock
    def test_post_success(self):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json={"audio_url": "https://example.com/audio.mp3"})
        )
        client = FishClient(api_token="test-token")
        result = client.post("/fish/tts", {"text": "Hello"})
        assert result["audio_url"] == "https://example.com/audio.mp3"

    @respx.mock
    def test_post_401(self):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = FishClient(api_token="bad-token")
        with pytest.raises(FishAuthError, match="Invalid API token"):
            client.post("/fish/tts", {"text": "test"})

    @respx.mock
    def test_post_403(self):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = FishClient(api_token="test-token")
        with pytest.raises(FishAuthError, match="Access denied"):
            client.post("/fish/tts", {"text": "test"})

    @respx.mock
    def test_post_500(self):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = FishClient(api_token="test-token")
        with pytest.raises(FishAPIError) as exc_info:
            client.post("/fish/tts", {"text": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_post_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/fish/tts").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = FishClient(api_token="test-token")
        with pytest.raises(FishTimeoutError):
            client.post("/fish/tts", {"text": "test"}, timeout=1)

    @respx.mock
    def test_post_removes_none_values(self):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json={"audio_url": "https://example.com/audio.mp3"})
        )
        client = FishClient(api_token="test-token")
        client.post("/fish/tts", {"text": "Hello", "reference_id": None})
        sent_payload = __import__("json").loads(route.calls[0].request.content)
        assert "reference_id" not in sent_payload

    @respx.mock
    def test_get_success(self):
        respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json={"total": 0, "items": []})
        )
        client = FishClient(api_token="test-token")
        result = client.get("/fish/model")
        assert result["total"] == 0

    @respx.mock
    def test_get_with_params(self):
        route = respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json={"total": 0, "items": []})
        )
        client = FishClient(api_token="test-token")
        client.get("/fish/model", params={"language": "en", "page_size": 10, "extra": None})
        request = route.calls[0].request
        assert "language=en" in str(request.url)
        assert "extra" not in str(request.url)

    @respx.mock
    def test_synthesize(self):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(
                200, json={"audio_url": "https://example.com/audio.mp3"}
            )
        )
        client = FishClient(api_token="test-token")
        result = client.synthesize(model="s2-pro", text="Hello")
        assert result["audio_url"] == "https://example.com/audio.mp3"

    @respx.mock
    def test_list_voices(self):
        respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json={"total": 1, "items": [{"_id": "v1"}]})
        )
        client = FishClient(api_token="test-token")
        result = client.list_voices(language="en")
        assert result["total"] == 1

    @respx.mock
    def test_get_voice(self):
        respx.get("https://api.acedata.cloud/fish/model/voice-123").mock(
            return_value=Response(200, json={"_id": "voice-123", "title": "Test"})
        )
        client = FishClient(api_token="test-token")
        result = client.get_voice("voice-123")
        assert result["_id"] == "voice-123"

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json={"success": True, "data": [{"id": "t-1"}]})
        )
        client = FishClient(api_token="test-token")
        result = client.query_task(id="t-1", action="retrieve")
        assert result["data"][0]["id"] == "t-1"

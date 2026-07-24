"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from producer_cli.core.client import ProducerClient
from producer_cli.core.exceptions import (
    ProducerAPIError,
    ProducerAuthError,
    ProducerTimeoutError,
)


class TestProducerClient:
    """Tests for ProducerClient."""

    def test_init_default(self):
        client = ProducerClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = ProducerClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = ProducerClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = ProducerClient(api_token="")
        with pytest.raises(ProducerAuthError):
            client._get_headers()

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json={"success": True, "task_id": "t-123"})
        )
        client = ProducerClient(api_token="test-token")
        result = client.request("/producer/audios", {"action": "generate", "prompt": "test"})
        assert result["success"] is True
        assert result["task_id"] == "t-123"

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = ProducerClient(api_token="bad-token")
        with pytest.raises(ProducerAuthError, match="Invalid API token"):
            client.request("/producer/audios", {"action": "generate", "prompt": "test"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = ProducerClient(api_token="test-token")
        with pytest.raises(ProducerAuthError, match="Access denied"):
            client.request("/producer/audios", {"action": "generate", "prompt": "test"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = ProducerClient(api_token="test-token")
        with pytest.raises(ProducerAPIError) as exc_info:
            client.request("/producer/audios", {"action": "generate", "prompt": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/producer/audios").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = ProducerClient(api_token="test-token")
        with pytest.raises(ProducerTimeoutError):
            client.request(
                "/producer/audios", {"action": "generate", "prompt": "test"}, timeout=1
            )

    @respx.mock
    def test_request_removes_none_values(self):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json={"success": True})
        )
        client = ProducerClient(api_token="test-token")
        result = client.request(
            "/producer/audios",
            {"action": "generate", "prompt": "test", "callback_url": None},
        )
        assert result["success"] is True

    @respx.mock
    def test_generate_audio(self):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json={"success": True, "task_id": "gen-123"})
        )
        client = ProducerClient(api_token="test-token")
        result = client.generate_audio(action="generate", prompt="test")
        assert result["task_id"] == "gen-123"

    @respx.mock
    def test_query_task(self):
        respx.post("https://api.acedata.cloud/producer/tasks").mock(
            return_value=Response(200, json={"success": True, "data": [{"id": "t-1"}]})
        )
        client = ProducerClient(api_token="test-token")
        result = client.query_task(id="t-1", action="retrieve")
        assert result["data"][0]["id"] == "t-1"

    @respx.mock
    def test_generate_lyrics(self):
        respx.post("https://api.acedata.cloud/producer/lyrics").mock(
            return_value=Response(
                200,
                json={"success": True, "data": {"text": "test lyrics", "title": "Test"}},
            )
        )
        client = ProducerClient(api_token="test-token")
        result = client.generate_lyrics(prompt="test")
        assert result["data"]["text"] == "test lyrics"

    @respx.mock
    def test_upload_audio(self):
        respx.post("https://api.acedata.cloud/producer/upload").mock(
            return_value=Response(
                200,
                json={"success": True, "data": {"audio_id": "uploaded-123"}},
            )
        )
        client = ProducerClient(api_token="test-token")
        result = client.upload_audio(audio_url="https://example.com/test.mp3")
        assert result["data"]["audio_id"] == "uploaded-123"

    @respx.mock
    def test_generate_video(self):
        respx.post("https://api.acedata.cloud/producer/videos").mock(
            return_value=Response(
                200,
                json={"success": True, "task_id": "vid-123"},
            )
        )
        client = ProducerClient(api_token="test-token")
        result = client.generate_video(audio_id="audio-abc")
        assert result["task_id"] == "vid-123"

    @respx.mock
    def test_get_wav(self):
        respx.post("https://api.acedata.cloud/producer/wav").mock(
            return_value=Response(
                200,
                json={"success": True, "task_id": "wav-123"},
            )
        )
        client = ProducerClient(api_token="test-token")
        result = client.get_wav(audio_id="audio-abc")
        assert result["task_id"] == "wav-123"

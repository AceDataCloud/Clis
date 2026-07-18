"""Tests for Kimi CLI client."""

import pytest
import respx
from httpx import Response

from kimi_cli.core.client import KimiClient, get_client
from kimi_cli.core.exceptions import KimiAPIError, KimiAuthError


class TestKimiClient:
    """Tests for KimiClient."""

    def test_client_init_with_token(self):
        client = KimiClient(api_token="test-token")
        assert client.api_token == "test-token"

    def test_client_init_default(self):
        client = KimiClient()
        assert client.base_url == "https://api.acedata.cloud"

    def test_get_client_with_token(self):
        client = get_client("test-token")
        assert client.api_token == "test-token"

    def test_get_headers_no_token(self):
        client = KimiClient(api_token="")
        with pytest.raises(KimiAuthError):
            client._get_headers()

    @respx.mock
    def test_chat_completions(self):
        mock_response = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "choices": [{"message": {"role": "assistant", "content": "Hello!"}}],
        }
        respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_response)
        )
        client = KimiClient(api_token="test-token")
        result = client.chat_completions(
            model="kimi-k2.6",
            messages=[{"role": "user", "content": "Hi"}],
        )
        assert result["id"] == "chatcmpl-test"

    @respx.mock
    def test_request_401_raises_auth_error(self):
        respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        client = KimiClient(api_token="bad-token")
        with pytest.raises(KimiAuthError):
            client.chat_completions(model="kimi-k2.6", messages=[])

    @respx.mock
    def test_request_403_raises_auth_error(self):
        respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(403, json={"error": "Forbidden"})
        )
        client = KimiClient(api_token="test-token")
        with pytest.raises(KimiAuthError):
            client.chat_completions(model="kimi-k2.6", messages=[])

    @respx.mock
    def test_request_500_raises_api_error(self):
        respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = KimiClient(api_token="test-token")
        with pytest.raises(KimiAPIError):
            client.chat_completions(model="kimi-k2.6", messages=[])

    @respx.mock
    def test_request_strips_none_values(self):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json={"choices": []})
        )
        client = KimiClient(api_token="test-token")
        client.chat_completions(
            model="kimi-k2.6",
            messages=[],
            temperature=None,
            top_p=None,
        )
        sent = route.calls[0].request.content
        import json

        payload = json.loads(sent)
        assert "temperature" not in payload
        assert "top_p" not in payload

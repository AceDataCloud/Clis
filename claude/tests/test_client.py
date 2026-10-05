"""Tests for the HTTP client."""

import json

import pytest
import respx
from httpx import Response

from claude_cli.core.client import ClaudeClient, get_client
from claude_cli.core.exceptions import ClaudeAPIError, ClaudeAuthError


class TestClaudeClient:
    """Tests for ClaudeClient."""

    def test_init_with_token(self):
        client = ClaudeClient(api_token="test-token")
        assert client.api_token == "test-token"

    def test_init_with_base_url(self):
        client = ClaudeClient(api_token="test-token", base_url="https://custom.example.com")
        assert client.base_url == "https://custom.example.com"

    def test_get_headers_with_token(self):
        client = ClaudeClient(api_token="test-token")
        headers = client._get_headers()
        assert "authorization" in headers
        assert "test-token" in headers["authorization"]
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token_raises(self):
        client = ClaudeClient(api_token="")
        with pytest.raises(ClaudeAuthError):
            client._get_headers()

    @respx.mock
    def test_chat_completions(self):
        mock_response = {"choices": [{"message": {"content": "Hello"}}]}
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_response)
        )
        client = ClaudeClient(api_token="test-token")
        result = client.chat_completions(model="claude-3-5-haiku-20241022", messages=[])
        assert result == mock_response

    @respx.mock
    def test_messages(self):
        mock_response = {"content": [{"type": "text", "text": "Hello"}]}
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_response)
        )
        client = ClaudeClient(api_token="test-token")
        result = client.messages(
            model="claude-3-5-haiku-20241022",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=1024,
        )
        assert result == mock_response
        assert "anthropic-beta" not in route.calls[0].request.headers

    @respx.mock
    def test_count_tokens(self):
        mock_response = {"input_tokens": 10}
        respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_response)
        )
        client = ClaudeClient(api_token="test-token")
        result = client.count_tokens(
            model="claude-3-5-haiku-20241022",
            messages=[{"role": "user", "content": "Hi"}],
        )
        assert result == mock_response

    @pytest.mark.parametrize(
        ("method", "endpoint", "response_fixture"),
        [
            ("messages", "/v1/messages", "mock_messages_response"),
            ("count_tokens", "/v1/messages/count_tokens", "mock_count_tokens_response"),
        ],
    )
    @respx.mock
    def test_thinking_and_beta_passthrough(self, method, endpoint, response_fixture, request):
        response = request.getfixturevalue(response_fixture)
        route = respx.post(f"https://api.acedata.cloud{endpoint}").mock(
            return_value=Response(200, json=response)
        )
        client = ClaudeClient(api_token="test-token")
        thinking = {"type": "between_tools", "display": "updates", "extension": {"value": 1}}
        beta = "thinking-display-updates-2026-08-18"
        result = getattr(client, method)(
            model="claude-opus-5",
            messages=[{"role": "user", "content": "Hi"}],
            thinking=thinking,
            anthropic_beta=beta,
        )
        assert result == response
        sent = route.calls[0].request
        assert sent.headers["anthropic-beta"] == beta
        assert sent.headers["authorization"] == "Bearer test-token"
        body = json.loads(sent.content)
        assert body["thinking"] == thinking
        assert "anthropic_beta" not in body
        assert "anthropic-beta" not in body

    @respx.mock
    def test_401_raises_auth_error(self):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        client = ClaudeClient(api_token="bad-token")
        with pytest.raises(ClaudeAuthError):
            client.chat_completions(model="claude-3-5-haiku-20241022", messages=[])

    @respx.mock
    def test_403_raises_auth_error(self):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(403, json={"error": "Forbidden"})
        )
        client = ClaudeClient(api_token="test-token")
        with pytest.raises(ClaudeAuthError):
            client.chat_completions(model="claude-3-5-haiku-20241022", messages=[])

    @respx.mock
    def test_500_raises_api_error(self):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = ClaudeClient(api_token="test-token")
        with pytest.raises(ClaudeAPIError):
            client.chat_completions(model="claude-3-5-haiku-20241022", messages=[])

    def test_none_values_removed_from_payload(self):
        """Verify None values are stripped from request payload."""
        payload = {"model": "claude-3-5-haiku-20241022", "temperature": None, "top_p": None}
        cleaned = {k: v for k, v in payload.items() if v is not None}
        assert "temperature" not in cleaned
        assert "top_p" not in cleaned
        assert "model" in cleaned


class TestGetClient:
    """Tests for the get_client factory function."""

    def test_get_client_with_token(self):
        client = get_client("my-token")
        assert isinstance(client, ClaudeClient)
        assert client.api_token == "my-token"

    def test_get_client_without_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "env-token")
        client = get_client()
        assert isinstance(client, ClaudeClient)

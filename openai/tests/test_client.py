"""Tests for the OpenAI client."""

import pytest
import respx
from httpx import Response

from openai_cli.core.client import OpenAIClient, get_client
from openai_cli.core.exceptions import OpenAIAPIError, OpenAIAuthError, OpenAITimeoutError


class TestOpenAIClient:
    """Tests for OpenAIClient."""

    def test_init_with_token(self):
        client = OpenAIClient(api_token="test-token")
        assert client.api_token == "test-token"

    def test_init_without_token(self):
        client = OpenAIClient(api_token="")
        assert client.api_token == ""

    def test_get_headers_with_token(self):
        client = OpenAIClient(api_token="test-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_without_token(self):
        client = OpenAIClient(api_token="")
        with pytest.raises(OpenAIAuthError):
            client._get_headers()

    @respx.mock
    def test_chat_success(self):
        mock_response = {"choices": [{"message": {"content": "Hello!"}}]}
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_response)
        )
        client = OpenAIClient(api_token="test-token")
        result = client.chat(model="gpt-4o-mini", messages=[{"role": "user", "content": "Hi"}])
        assert result == mock_response

    @respx.mock
    def test_embed_success(self):
        mock_response = {"data": [{"embedding": [0.1, 0.2]}], "model": "text-embedding-3-small"}
        respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_response)
        )
        client = OpenAIClient(api_token="test-token")
        result = client.embed(model="text-embedding-3-small", input="Hello")
        assert result == mock_response

    @respx.mock
    def test_generate_image_success(self):
        mock_response = {"data": [{"url": "https://example.com/img.png"}]}
        respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_response)
        )
        client = OpenAIClient(api_token="test-token")
        result = client.generate_image(prompt="A cat", model="dall-e-3")
        assert result == mock_response

    @respx.mock
    def test_edit_image_success(self):
        mock_response = {"data": [{"url": "https://example.com/edited.png"}]}
        respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_response)
        )
        client = OpenAIClient(api_token="test-token")
        result = client.edit_image(prompt="Remove background", image="https://example.com/src.jpg")
        assert result == mock_response

    @respx.mock
    def test_respond_success(self):
        mock_response = {"choices": [{"message": {"content": "Paris"}}]}
        respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_response)
        )
        client = OpenAIClient(api_token="test-token")
        result = client.respond(
            model="gpt-4o-mini", input=[{"role": "user", "content": "Capital of France?"}]
        )
        assert result == mock_response

    @respx.mock
    def test_auth_error_401(self):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        client = OpenAIClient(api_token="bad-token")
        with pytest.raises(OpenAIAuthError):
            client.chat(model="gpt-4o-mini", messages=[])

    @respx.mock
    def test_auth_error_403(self):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(403, json={"error": "Forbidden"})
        )
        client = OpenAIClient(api_token="bad-token")
        with pytest.raises(OpenAIAuthError):
            client.chat(model="gpt-4o-mini", messages=[])

    @respx.mock
    def test_api_error_500(self):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = OpenAIClient(api_token="test-token")
        with pytest.raises(OpenAIAPIError):
            client.chat(model="gpt-4o-mini", messages=[])

    def test_none_values_removed_from_payload(self):
        """None values should be removed from the request payload."""
        client = OpenAIClient(api_token="test-token")
        payload = {"model": "gpt-4o-mini", "temperature": None, "max_tokens": None}
        cleaned = {k: v for k, v in payload.items() if v is not None}
        assert "temperature" not in cleaned
        assert "max_tokens" not in cleaned
        assert cleaned["model"] == "gpt-4o-mini"


class TestGetClient:
    """Tests for get_client factory function."""

    def test_get_client_with_token(self):
        client = get_client("my-token")
        assert client.api_token == "my-token"

    def test_get_client_without_token(self):
        client = get_client()
        assert isinstance(client, OpenAIClient)

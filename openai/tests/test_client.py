"""Tests for the HTTP client."""

import pytest
import respx
from httpx import Response

from openai_cli.core.client import OpenAIClient, get_client
from openai_cli.core.exceptions import OpenAIAPIError, OpenAIAuthError


class TestOpenAIClient:
    """Tests for the OpenAI API client."""

    def test_get_client_with_token(self):
        client = get_client("test-token")
        assert client.api_token == "test-token"

    def test_get_client_without_token(self):
        client = get_client()
        assert isinstance(client, OpenAIClient)

    def test_missing_token_raises_auth_error(self):
        client = OpenAIClient(api_token="")
        with pytest.raises(OpenAIAuthError):
            client._get_headers()

    @respx.mock
    def test_chat_completions_request(self):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(
                200,
                json={"choices": [{"message": {"role": "assistant", "content": "Hello"}}]},
            )
        )
        client = OpenAIClient(api_token="test-token")
        result = client.chat_completions(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
        )
        assert route.called
        assert "choices" in result

    @respx.mock
    def test_embeddings_request(self):
        route = respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(
                200,
                json={"data": [{"embedding": [0.1, 0.2]}], "object": "list"},
            )
        )
        client = OpenAIClient(api_token="test-token")
        result = client.embeddings(model="text-embedding-3-small", input="Hello")
        assert route.called
        assert "data" in result

    @respx.mock
    def test_unauthorized_raises_auth_error(self):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        client = OpenAIClient(api_token="bad-token")
        with pytest.raises(OpenAIAuthError):
            client.chat_completions(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hi"}],
            )

    @respx.mock
    def test_api_error_raises_api_error(self):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(400, text="Bad request")
        )
        client = OpenAIClient(api_token="test-token")
        with pytest.raises(OpenAIAPIError):
            client.chat_completions(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hi"}],
            )

    def test_none_values_stripped_from_payload(self):
        payload = {"model": "gpt-4o-mini", "temperature": None, "n": None}
        stripped = {k: v for k, v in payload.items() if v is not None}
        assert "temperature" not in stripped
        assert "n" not in stripped
        assert "model" in stripped

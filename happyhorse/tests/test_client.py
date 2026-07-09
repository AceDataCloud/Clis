"""Tests for HappyHorse HTTP client."""

import pytest
import respx
from httpx import Response

from happyhorse_cli.core.client import HappyHorseClient, get_client
from happyhorse_cli.core.exceptions import HappyHorseAuthError


class TestHappyHorseClient:
    """Tests for HappyHorseClient."""

    def test_init_with_token(self):
        client = HappyHorseClient(api_token="test-token")
        assert client.api_token == "test-token"

    def test_get_headers(self):
        client = HappyHorseClient(api_token="test-token")
        headers = client._get_headers()
        assert "Bearer" in headers["authorization"]
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self):
        client = HappyHorseClient(api_token="")
        with pytest.raises(HappyHorseAuthError):
            client._get_headers()

    @respx.mock
    def test_generate_video(self):
        mock_response = {"success": True, "task_id": "task-123"}
        respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_response)
        )
        client = HappyHorseClient(api_token="test-token")
        result = client.generate_video(action="generate", prompt="test")
        assert result["success"] is True
        assert result["task_id"] == "task-123"

    @respx.mock
    def test_query_task(self):
        mock_response = {"success": True, "data": {"id": "task-123", "status": "completed"}}
        respx.post("https://api.acedata.cloud/happyhorse/tasks").mock(
            return_value=Response(200, json=mock_response)
        )
        client = HappyHorseClient(api_token="test-token")
        result = client.query_task(id="task-123", action="retrieve")
        assert result["success"] is True

    @respx.mock
    def test_unauthorized(self):
        respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = HappyHorseClient(api_token="bad-token")
        with pytest.raises(HappyHorseAuthError):
            client.generate_video(action="generate", prompt="test")

    @respx.mock
    def test_none_values_removed(self):
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json={"success": True, "task_id": "t1"})
        )
        client = HappyHorseClient(api_token="test-token")
        client.generate_video(action="generate", prompt="test", callback_url=None)
        import json

        sent = json.loads(route.calls[0].request.content)
        assert "callback_url" not in sent

    def test_get_client(self):
        client = get_client("my-token")
        assert isinstance(client, HappyHorseClient)
        assert client.api_token == "my-token"

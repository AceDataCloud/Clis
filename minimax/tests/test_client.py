"""Tests for MiniMax HTTP client."""

import pytest
import respx
from httpx import Response

from minimax_cli.core.client import MiniMaxClient, get_client
from minimax_cli.core.exceptions import MiniMaxAuthError


class TestMiniMaxClient:
    """Tests for MiniMaxClient."""

    def test_init_with_token(self):
        client = MiniMaxClient(api_token="test-token")
        assert client.api_token == "test-token"

    def test_get_headers(self):
        client = MiniMaxClient(api_token="test-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self):
        client = MiniMaxClient(api_token="")
        with pytest.raises(MiniMaxAuthError):
            client._get_headers()

    @respx.mock
    def test_generate_video(self):
        mock_response = {"success": True, "task_id": "task-123"}
        respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_response)
        )
        client = MiniMaxClient(api_token="test-token")
        result = client.generate_video(prompt="test")
        assert result["success"] is True
        assert result["task_id"] == "task-123"

    @respx.mock
    def test_query_task(self):
        mock_response = {"success": True, "data": {"id": "task-123", "status": "completed"}}
        respx.post("https://api.acedata.cloud/minimax/tasks").mock(
            return_value=Response(200, json=mock_response)
        )
        client = MiniMaxClient(api_token="test-token")
        result = client.query_task(id="task-123", action="retrieve")
        assert result["success"] is True

    @respx.mock
    def test_unauthorized(self):
        respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = MiniMaxClient(api_token="bad-token")
        with pytest.raises(MiniMaxAuthError):
            client.generate_video(prompt="test")

    @respx.mock
    def test_none_values_removed(self):
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json={"success": True, "task_id": "t1"})
        )
        client = MiniMaxClient(api_token="test-token")
        client.generate_video(prompt="test", callback_url=None)
        import json

        sent = json.loads(route.calls[0].request.content)
        assert "callback_url" not in sent

    def test_get_client(self):
        client = get_client("my-token")
        assert isinstance(client, MiniMaxClient)
        assert client.api_token == "my-token"

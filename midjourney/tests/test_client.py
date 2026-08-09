"""Unit tests for HTTP client."""

from unittest.mock import MagicMock, patch

import pytest

from midjourney_cli.core.client import MidjourneyClient
from midjourney_cli.core.exceptions import MidjourneyAuthError


@pytest.fixture
def client() -> MidjourneyClient:
    return MidjourneyClient(api_token="test-token", base_url="https://api.test.local")


class TestMidjourneyClient:
    """Tests for MidjourneyClient class."""

    def test_get_headers(self, client):
        """Test that headers are correctly generated."""
        headers = client._get_headers()
        assert headers["accept"] == "application/json"
        assert "authorization" in headers
        assert headers["content-type"] == "application/json"

    def test_get_headers_with_accept_override(self, client):
        """Test that the documented Accept header can be overridden."""
        headers = client._get_headers("application/x-ndjson")
        assert headers["accept"] == "application/x-ndjson"

    def test_get_headers_no_token(self):
        """Test that missing token raises auth error."""
        client = MidjourneyClient(api_token="", base_url="https://api.test.local")
        with pytest.raises(MidjourneyAuthError, match="not configured"):
            client._get_headers()

    def test_request_uses_accept_header_override(self, client):
        """Test accept is sent as a header and not as a JSON body field."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}

        with patch("httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__enter__.return_value = mock_instance

            result = client.imagine(accept="application/x-ndjson", prompt="test")

            assert result == {"success": True}
            call_args = mock_instance.post.call_args
            assert "/midjourney/imagine" in call_args[0][0]
            assert call_args[1]["headers"]["accept"] == "application/x-ndjson"
            assert call_args[1]["json"] == {"prompt": "test"}

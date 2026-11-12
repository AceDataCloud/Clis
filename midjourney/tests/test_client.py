"""Unit tests for HTTP client."""

from unittest.mock import MagicMock, patch

import pytest

from midjourney_cli.core.client import MidjourneyClient
from midjourney_cli.core.exceptions import MidjourneyAuthError, MidjourneyError


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

    @pytest.mark.parametrize("model", ["8.2", "", None])
    @pytest.mark.parametrize("async_mode", [False, True])
    @pytest.mark.parametrize("entry_point", ["imagine", "request"])
    def test_imagine_rejects_model_before_request(self, client, model, async_mode, entry_point):
        payload = {
            "prompt": "test",
            "version": "8.2",
            "model": model,
            "async": async_mode,
            "accept": "application/json",
        }
        original_payload = payload.copy()

        with patch("httpx.Client") as mock_http:
            with pytest.raises(MidjourneyError, match="use 'version' instead") as error:
                if entry_point == "imagine":
                    client.imagine(**payload)
                else:
                    client.request("/midjourney/imagine", payload)

            assert error.value.code == "bad_request"
            mock_http.assert_not_called()
        assert payload == original_payload

    @pytest.mark.parametrize("version", [None, "8.2"])
    @pytest.mark.parametrize("async_mode", [False, True])
    def test_imagine_version_payload(self, client, mock_imagine_response, version, async_mode):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_imagine_response
        payload = {"prompt": "test", "version": version, "async": async_mode}

        with patch("httpx.Client") as mock_http:
            mock_instance = mock_http.return_value.__enter__.return_value
            mock_instance.post.return_value = mock_response

            assert client.imagine(**payload) == mock_imagine_response
            body = mock_instance.post.call_args.kwargs["json"]
            assert "model" not in body
            assert body["async"] is async_mode
            if version is None:
                assert "version" not in body
            else:
                assert body["version"] == version

    def test_model_guard_is_scoped_to_imagine(self, client, mock_task_response):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_task_response

        with patch("httpx.Client") as mock_http:
            mock_instance = mock_http.return_value.__enter__.return_value
            mock_instance.post.return_value = mock_response

            assert client.query_task(id="test-task-123", model=None) == mock_task_response
            assert mock_instance.post.call_args.kwargs["json"] == {"id": "test-task-123"}

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

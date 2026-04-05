"""Tests for HTTP client."""

import pytest
import respx
from httpx import Response

from serp_cli.core.client import SerpClient
from serp_cli.core.exceptions import (
    SerpAPIError,
    SerpAuthError,
    SerpTimeoutError,
)


class TestSerpClient:
    """Tests for SerpClient."""

    def test_init_default(self):
        client = SerpClient(api_token="test-token")
        assert client.api_token == "test-token"
        assert client.base_url == "https://api.acedata.cloud"

    def test_init_custom(self):
        client = SerpClient(api_token="tok", base_url="https://custom.api")
        assert client.api_token == "tok"
        assert client.base_url == "https://custom.api"

    def test_headers(self):
        client = SerpClient(api_token="my-token")
        headers = client._get_headers()
        assert headers["authorization"] == "Bearer my-token"
        assert headers["content-type"] == "application/json"

    def test_headers_no_token(self):
        client = SerpClient(api_token="")
        with pytest.raises(SerpAuthError):
            client._get_headers()

    @respx.mock
    def test_request_success(self):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json={"organic": [{"title": "test"}]})
        )
        client = SerpClient(api_token="test-token")
        result = client.request("/serp/google", {"query": "test"})
        assert "organic" in result

    @respx.mock
    def test_request_401(self):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        client = SerpClient(api_token="bad-token")
        with pytest.raises(SerpAuthError, match="Invalid API token"):
            client.request("/serp/google", {"query": "test"})

    @respx.mock
    def test_request_403(self):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(403, json={"error": "forbidden"})
        )
        client = SerpClient(api_token="test-token")
        with pytest.raises(SerpAuthError, match="Access denied"):
            client.request("/serp/google", {"query": "test"})

    @respx.mock
    def test_request_500(self):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        client = SerpClient(api_token="test-token")
        with pytest.raises(SerpAPIError) as exc_info:
            client.request("/serp/google", {"query": "test"})
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_request_timeout(self):
        import httpx

        respx.post("https://api.acedata.cloud/serp/google").mock(
            side_effect=httpx.TimeoutException("timeout")
        )
        client = SerpClient(api_token="test-token")
        with pytest.raises(SerpTimeoutError):
            client.request("/serp/google", {"query": "test"}, timeout=1)

    @respx.mock
    def test_request_removes_none_values(self):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json={"organic": []})
        )
        client = SerpClient(api_token="test-token")
        result = client.request(
            "/serp/google",
            {"query": "test", "country": None, "language": None},
        )
        assert "organic" in result

    @respx.mock
    def test_search(self):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json={"organic": [{"title": "Result"}]})
        )
        client = SerpClient(api_token="test-token")
        result = client.search(query="test", type="search")
        assert "organic" in result

    @respx.mock
    def test_search_with_params(self):
        import json

        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json={"organic": []})
        )
        client = SerpClient(api_token="test-token")
        client.search(query="test", type="news", country="uk", language="en", number=20)
        body = json.loads(route.calls.last.request.content)
        assert body["query"] == "test"
        assert body["type"] == "news"
        assert body["country"] == "uk"
        assert body["number"] == 20

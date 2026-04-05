"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from serp_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "serp-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "search" in result.output
        assert "images" in result.output
        assert "news" in result.output

    def test_help_search(self, runner):
        result = runner.invoke(cli, ["search", "--help"])
        assert result.exit_code == 0
        assert "QUERY" in result.output
        assert "--type" in result.output
        assert "--country" in result.output


# ─── Search Commands ──────────────────────────────────────────────────────


class TestSearchCommands:
    """Tests for search commands."""

    @respx.mock
    def test_search_json(self, runner, mock_search_response):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "search", "artificial intelligence", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "organic" in data

    @respx.mock
    def test_search_rich_output(self, runner, mock_search_response):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "search", "artificial intelligence"])
        assert result.exit_code == 0
        assert "Artificial Intelligence" in result.output

    @respx.mock
    def test_search_with_type(self, runner, mock_news_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_news_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "search", "tech news", "-t", "news", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["type"] == "news"

    @respx.mock
    def test_search_with_country(self, runner, mock_search_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "search", "test", "-c", "uk", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["country"] == "uk"

    @respx.mock
    def test_search_with_number(self, runner, mock_search_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "search", "test", "-n", "20", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["number"] == 20

    def test_search_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "search", "test"])
        assert result.exit_code != 0


# ─── Shortcut Commands ────────────────────────────────────────────────────


class TestShortcutCommands:
    """Tests for shortcut search commands."""

    @respx.mock
    def test_images(self, runner, mock_images_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_images_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "images", "sunset", "--json"])
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["type"] == "images"

    @respx.mock
    def test_news(self, runner, mock_news_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_news_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "news", "AI news", "--json"])
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["type"] == "news"

    @respx.mock
    def test_videos(self, runner, mock_search_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "videos", "how to cook", "--json"])
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["type"] == "videos"

    @respx.mock
    def test_places(self, runner, mock_search_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "places", "coffee shops", "--json"])
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["type"] == "places"

    @respx.mock
    def test_maps(self, runner, mock_search_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "maps", "Eiffel Tower", "--json"])
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["type"] == "maps"


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_search_types(self, runner):
        result = runner.invoke(cli, ["search-types"])
        assert result.exit_code == 0
        assert "search" in result.output
        assert "images" in result.output
        assert "news" in result.output

    def test_time_ranges(self, runner):
        result = runner.invoke(cli, ["time-ranges"])
        assert result.exit_code == 0
        assert "qdr:h" in result.output
        assert "qdr:d" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

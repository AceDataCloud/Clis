"""Tests for TikTok CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from tiktok_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def ok() -> dict[str, object]:
    return {"data": []}


def test_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for command in ["posts", "search", "user", "video"]:
        assert command in result.output


@respx.mock
def test_posts_payload(runner):
    route = respx.post("https://api.acedata.cloud/tiktok/posts").mock(return_value=Response(200, json=ok()))
    result = runner.invoke(cli, ["--token", "test-token", "posts", "--unique-id", "acedata", "--cursor", "10", "--json"])
    assert result.exit_code == 0
    sent = json.loads(route.calls[0].request.content)
    assert sent == {"cursor": "10", "unique_id": "acedata"}


@respx.mock
def test_search_payload(runner):
    route = respx.post("https://api.acedata.cloud/tiktok/search").mock(return_value=Response(200, json=ok()))
    result = runner.invoke(cli, ["--token", "test-token", "search", "cats", "--type", "video", "--region", "us", "--sort-type", "3", "--publish-time", "24", "--json"])
    assert result.exit_code == 0
    sent = json.loads(route.calls[0].request.content)
    assert sent["keywords"] == "cats"
    assert sent["type"] == "video"
    assert sent["sort_type"] == 3
    assert sent["publish_time"] == 24


@respx.mock
def test_user_payload(runner):
    route = respx.post("https://api.acedata.cloud/tiktok/user").mock(return_value=Response(200, json=ok()))
    result = runner.invoke(cli, ["--token", "test-token", "user", "--user-id", "123", "--json"])
    assert result.exit_code == 0
    sent = json.loads(route.calls[0].request.content)
    assert sent == {"user_id": "123"}


@respx.mock
def test_video_payload(runner):
    route = respx.post("https://api.acedata.cloud/tiktok/video").mock(return_value=Response(200, json=ok()))
    result = runner.invoke(cli, ["--token", "test-token", "video", "https://tiktok.test/v/1", "--original-quality", "1", "--json"])
    assert result.exit_code == 0
    sent = json.loads(route.calls[0].request.content)
    assert sent == {"video_url": "https://tiktok.test/v/1", "original_quality": 1}

"""Tests for Twitter/X CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from tw_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def ok() -> dict[str, object]:
    return {"data": []}


def test_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for command in ["posts", "users", "retweets"]:
        assert command in result.output


@respx.mock
def test_posts_payload(runner):
    route = respx.post("https://api.acedata.cloud/x/posts").mock(return_value=Response(200, json=ok()))
    result = runner.invoke(cli, ["--token", "test-token", "posts", "123", "--cursor", "abc", "--json"])
    assert result.exit_code == 0
    sent = json.loads(route.calls[0].request.content)
    assert sent == {"user_id": "123", "cursor": "abc"}


@respx.mock
def test_users_payload(runner):
    route = respx.post("https://api.acedata.cloud/x/users").mock(return_value=Response(200, json=ok()))
    result = runner.invoke(cli, ["--token", "test-token", "users", "acedata", "--json"])
    assert result.exit_code == 0
    sent = json.loads(route.calls[0].request.content)
    assert sent == {"username": "acedata"}


@respx.mock
def test_retweets_payload(runner):
    route = respx.post("https://api.acedata.cloud/x/retweets").mock(return_value=Response(200, json=ok()))
    result = runner.invoke(cli, ["--token", "test-token", "retweets", "1894625520991547884", "--cursor", "abc", "--json"])
    assert result.exit_code == 0
    sent = json.loads(route.calls[0].request.content)
    assert sent == {"post_id": "1894625520991547884", "cursor": "abc"}

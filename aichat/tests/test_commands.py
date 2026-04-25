"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from aichat_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "aichat-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "models" in result.output
        assert "config" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "QUESTION" in result.output
        assert "--model" in result.output
        assert "--stateful" in result.output


# ─── Chat Command ─────────────────────────────────────────────────────────


class TestChatCommands:
    """Tests for the chat command."""

    @respx.mock
    def test_chat_json(self, runner, mock_conversation_response):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is AI?", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "answer" in data
        assert "id" in data

    @respx.mock
    def test_chat_rich_output(self, runner, mock_conversation_response):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "What is AI?"])
        assert result.exit_code == 0
        assert "highly intelligent" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_conversation_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "-m", "gpt-4o", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-4o"

    @respx.mock
    def test_chat_with_conversation_id(self, runner, mock_conversation_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Continue",
                "--id",
                "some-id-123",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["id"] == "some-id-123"

    @respx.mock
    def test_chat_stateful(self, runner, mock_conversation_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello!", "--stateful", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["stateful"] is True

    @respx.mock
    def test_chat_with_references(self, runner, mock_conversation_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Summarize",
                "-r",
                "https://example.com/article",
                "-r",
                "https://example.com/another",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert "references" in body
        assert len(body["references"]) == 2

    @respx.mock
    def test_chat_with_preset(self, runner, mock_conversation_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--preset", "my-preset", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["preset"] == "my-preset"

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0

    @respx.mock
    def test_chat_conversation_id_shown(self, runner, mock_conversation_response):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_conversation_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "What is AI?"])
        assert result.exit_code == 0
        assert "64a67fff" in result.output


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gpt-4o" in result.output
        assert "deepseek-r1" in result.output
        assert "grok-3" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

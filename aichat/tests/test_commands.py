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
        assert "--id" in result.output


# ─── Chat Commands ────────────────────────────────────────────────────────


class TestChatCommands:
    """Tests for chat command."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "What is AI?", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "answer" in data
        assert "id" in data

    @respx.mock
    def test_chat_rich_output(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "What is AI?"])
        assert result.exit_code == 0
        assert "highly intelligent" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "-m", "gpt-4o-mini", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-4o-mini"

    @respx.mock
    def test_chat_with_conversation_id(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Tell me more",
                "--id",
                "abc-123",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["id"] == "abc-123"

    @respx.mock
    def test_chat_with_stateful(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--stateful", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["stateful"] is True

    @respx.mock
    def test_chat_with_references(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Summarize",
                "--ref",
                "https://example.com/doc.txt",
                "--ref",
                "Some text content",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["references"] == [
            "https://example.com/doc.txt",
            "Some text content",
        ]

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0

    @respx.mock
    def test_chat_sends_question(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        runner.invoke(
            cli,
            ["--token", "test-token", "chat", "What is the meaning of life?", "--json"],
        )
        body = json.loads(route.calls.last.request.content)
        assert body["question"] == "What is the meaning of life?"


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gpt-4o" in result.output
        assert "deepseek" in result.output.lower()

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

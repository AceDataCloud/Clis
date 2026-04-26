"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from claude_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "claude-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "messages" in result.output

    def test_chat_help(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_messages_help(self, runner):
        result = runner.invoke(cli, ["messages", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_count_tokens_help(self, runner):
        result = runner.invoke(cli, ["count-tokens", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output


class TestChatCommands:
    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "What is the capital of France?", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "choices" in data

    @respx.mock
    def test_chat_rich_output(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is the capital of France?"]
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--model", "claude-opus-4-20250514"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--system", "You are a helpful assistant."],
        )
        assert result.exit_code == 0

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["chat", "Hello"])
        assert result.exit_code != 0


class TestMessagesCommands:
    @respx.mock
    def test_messages_json(self, runner, mock_messages_response):
        respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "messages", "What is the capital of France?", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "content" in data

    @respx.mock
    def test_messages_rich_output(self, runner, mock_messages_response):
        respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "messages", "What is the capital of France?"],
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_messages_with_max_tokens(self, runner, mock_messages_response):
        respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "messages", "Hello", "--max-tokens", "2048"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_messages_with_system(self, runner, mock_messages_response):
        respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "Hello",
                "--system",
                "You are a helpful assistant.",
            ],
        )
        assert result.exit_code == 0


class TestCountTokensCommands:
    @respx.mock
    def test_count_tokens_json(self, runner, mock_count_tokens_response):
        respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "count-tokens", "What is the capital of France?", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "input_tokens" in data

    @respx.mock
    def test_count_tokens_rich_output(self, runner, mock_count_tokens_response):
        respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "count-tokens", "What is the capital of France?"],
        )
        assert result.exit_code == 0
        assert "42" in result.output


class TestInfoCommands:
    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "claude-sonnet-4-20250514" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

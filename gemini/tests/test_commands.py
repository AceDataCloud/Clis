"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from gemini_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "gemini-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "generate" in result.output

    def test_chat_help(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_generate_help(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output


class TestChatCommands:
    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
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
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is the capital of France?"]
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--model", "gemini-2.5-pro"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--system", "You are a helpful assistant."],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_temperature(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--temperature", "0.7"],
        )
        assert result.exit_code == 0

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["chat", "Hello"])
        assert result.exit_code != 0


class TestGenerateCommands:
    @respx.mock
    def test_generate_json(self, runner, mock_generate_response):
        respx.post(
            "https://api.acedata.cloud/v1beta/models/gemini-2.5-flash:generateContent"
        ).mock(return_value=Response(200, json=mock_generate_response))
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "What is the capital of France?", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "candidates" in data

    @respx.mock
    def test_generate_rich_output(self, runner, mock_generate_response):
        respx.post(
            "https://api.acedata.cloud/v1beta/models/gemini-2.5-flash:generateContent"
        ).mock(return_value=Response(200, json=mock_generate_response))
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "What is the capital of France?"],
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_generate_response):
        respx.post(
            "https://api.acedata.cloud/v1beta/models/gemini-2.5-pro:generateContent"
        ).mock(return_value=Response(200, json=mock_generate_response))
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "Hello", "--model", "gemini-2.5-pro"],
        )
        assert result.exit_code == 0


class TestInfoCommands:
    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gemini-2.5-flash" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

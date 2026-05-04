"""Tests for GLM CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from glm_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "glm-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output


class TestChatCommand:
    """Tests for chat commands."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is the capital of France?", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["choices"][0]["message"]["content"] == "The capital of France is Paris."

    @respx.mock
    def test_chat_rich_output(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello"]
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-m", "glm-5.1", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "chat", "Hello",
                "-s", "You are a helpful assistant", "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_temperature(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "--temperature", "0.5", "--json"]
        )
        assert result.exit_code == 0

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "glm-4.7" in result.output
        assert "glm-5.1" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

"""Tests for Kimi CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from kimi_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "kimi-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "models" in result.output
        assert "config" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output


class TestChatCommand:
    """Tests for chat commands."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
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
        respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "Hello"])
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-m", "kimi-k3", "--json"]
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "kimi-k3"

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "-s", "You are helpful", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["messages"][0]["role"] == "system"

    @respx.mock
    def test_chat_with_temperature(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "--temperature", "0.5", "--json"]
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["temperature"] == 0.5

    @respx.mock
    def test_chat_with_reasoning_effort(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--reasoning-effort", "max", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["reasoning_effort"] == "max"

    def test_chat_with_invalid_reasoning_effort(self, runner):
        result = runner.invoke(
            cli,
            ["chat", "Hello", "--reasoning-effort", "high"],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_chat_with_service_tier(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--service-tier", "flex", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["service_tier"] == "flex"

    @respx.mock
    def test_chat_with_logprobs(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "--logprobs",
                "--top-logprobs",
                "5",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["logprobs"] is True
        assert sent["top_logprobs"] == 5

    @respx.mock
    def test_chat_with_max_completion_tokens(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "--max-completion-tokens",
                "100",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["max_completion_tokens"] == 100

    @respx.mock
    def test_chat_with_parallel_tool_calls(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--parallel-tool-calls", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["parallel_tool_calls"] is True

    @respx.mock
    def test_chat_with_store(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--store", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["store"] is True

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "kimi-k3" in result.output
        assert "kimi-k2.6" in result.output
        assert "default" in result.output.lower()

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

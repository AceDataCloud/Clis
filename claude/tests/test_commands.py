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


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "claude-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "messages" in result.output
        assert "count-tokens" in result.output

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
        assert "--max-tokens" in result.output

    def test_count_tokens_help(self, runner):
        result = runner.invoke(cli, ["count-tokens", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_models_help(self, runner):
        result = runner.invoke(cli, ["models", "--help"])
        assert result.exit_code == 0

    def test_config_help(self, runner):
        result = runner.invoke(cli, ["config", "--help"])
        assert result.exit_code == 0


# ─── Chat Commands ────────────────────────────────────────────────────────


class TestChatCommands:
    """Tests for the chat command."""

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
        route = respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "-m",
                "claude-3-5-sonnet-20241022",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["model"] == "claude-3-5-sonnet-20241022"

    @respx.mock
    def test_chat_with_system(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "-s",
                "You are a helpful assistant.",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        messages = request_body["messages"]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a helpful assistant."

    @respx.mock
    def test_chat_with_temperature(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--temperature", "0.9"],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["temperature"] == 0.9

    @respx.mock
    def test_chat_with_reasoning_effort(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--reasoning-effort", "high"],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["reasoning_effort"] == "high"

    @respx.mock
    def test_chat_auth_error(self, runner):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        result = runner.invoke(
            cli, ["--token", "bad-token", "chat", "Hello"]
        )
        assert result.exit_code != 0

    def test_chat_no_token(self, runner, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        result = runner.invoke(cli, ["chat", "Hello"])
        assert result.exit_code != 0


# ─── Messages Commands ────────────────────────────────────────────────────


class TestMessagesCommands:
    """Tests for the messages command."""

    @respx.mock
    def test_messages_json(self, runner, mock_messages_response):
        respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "What is the capital of France?",
                "--json",
            ],
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
            cli, ["--token", "test-token", "messages", "What is the capital of France?"]
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_messages_with_max_tokens(self, runner, mock_messages_response):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "messages", "Hello", "--max-tokens", "2048"],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["max_tokens"] == 2048

    @respx.mock
    def test_messages_with_system(self, runner, mock_messages_response):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "Hello",
                "-s",
                "You are a helpful assistant.",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["system"] == "You are a helpful assistant."

    @respx.mock
    def test_messages_with_model(self, runner, mock_messages_response):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "messages", "Hello", "-m", "claude-3-5-sonnet-20241022"],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["model"] == "claude-3-5-sonnet-20241022"

    @respx.mock
    def test_messages_auth_error(self, runner):
        respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        result = runner.invoke(
            cli, ["--token", "bad-token", "messages", "Hello"]
        )
        assert result.exit_code != 0


# ─── Count Tokens Commands ────────────────────────────────────────────────


class TestCountTokensCommands:
    """Tests for the count-tokens command."""

    @respx.mock
    def test_count_tokens_json(self, runner, mock_count_tokens_response):
        respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "count-tokens", "Hello world", "--json"],
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
            cli, ["--token", "test-token", "count-tokens", "Hello world"]
        )
        assert result.exit_code == 0
        assert "15" in result.output

    @respx.mock
    def test_count_tokens_with_model(self, runner, mock_count_tokens_response):
        route = respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "count-tokens",
                "Hello",
                "-m",
                "claude-3-5-sonnet-20241022",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["model"] == "claude-3-5-sonnet-20241022"

    @respx.mock
    def test_count_tokens_with_system(self, runner, mock_count_tokens_response):
        route = respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "count-tokens",
                "Hello",
                "-s",
                "You are a summarizer.",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["system"] == "You are a summarizer."


# ─── Models / Config Commands ────────────────────────────────────────────


class TestInfoCommands:
    """Tests for models and config commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "claude" in result.output.lower()
        assert "claude-fable-5" in result.output

    def test_models_first_entry(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        lines = [line for line in result.output.splitlines() if "claude-" in line]
        assert "claude-fable-5" in lines[0]

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "API Token" in result.output
        assert "API Base URL" in result.output


# ─── Messages Thinking ────────────────────────────────────────────────────


class TestMessagesThinking:
    """Tests for the --thinking-type and --thinking-budget-tokens options."""

    @respx.mock
    def test_messages_with_thinking_enabled(self, runner, mock_messages_response):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "Think carefully",
                "--thinking-type",
                "enabled",
                "--thinking-budget-tokens",
                "2048",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["thinking"] == {"type": "enabled", "budget_tokens": 2048}

    @respx.mock
    def test_messages_with_thinking_disabled(self, runner, mock_messages_response):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "Hello",
                "--thinking-type",
                "disabled",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["thinking"] == {"type": "disabled"}

    @respx.mock
    def test_messages_with_thinking_adaptive(self, runner, mock_messages_response):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "Hello",
                "--thinking-type",
                "adaptive",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["thinking"] == {"type": "adaptive"}

    @respx.mock
    def test_messages_without_thinking(self, runner, mock_messages_response):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "messages", "Hello"]
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body.get("thinking") is None

    def test_messages_thinking_budget_below_minimum(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "Hello",
                "--thinking-type",
                "enabled",
                "--thinking-budget-tokens",
                "512",
            ],
        )
        assert result.exit_code != 0

    def test_messages_thinking_enabled_requires_budget(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "messages",
                "Hello",
                "--thinking-type",
                "enabled",
            ],
        )
        assert result.exit_code != 0
        assert "thinking-budget-tokens" in result.output

    @respx.mock
    def test_count_tokens_with_thinking_enabled(self, runner, mock_count_tokens_response):
        route = respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "count-tokens",
                "Hello",
                "--thinking-type",
                "enabled",
                "--thinking-budget-tokens",
                "1024",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["thinking"] == {"type": "enabled", "budget_tokens": 1024}

    @respx.mock
    def test_count_tokens_without_thinking(self, runner, mock_count_tokens_response):
        route = respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "count-tokens", "Hello"]
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body.get("thinking") is None

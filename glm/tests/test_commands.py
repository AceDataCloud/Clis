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
        assert "--max-completion-tokens" in result.output
        assert "--response-format" in result.output
        assert "--tool-choice" in result.output


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

    @respx.mock
    def test_chat_with_advanced_scalar_options(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "--stream",
                "--max-completion-tokens",
                "512",
                "--logprobs",
                "--top-logprobs",
                "3",
                "--parallel-tool-calls",
                "--reasoning-effort",
                "high",
                "--service-tier",
                "flex",
                "--store",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["stream"] is True
        assert body["max_completion_tokens"] == 512
        assert body["logprobs"] is True
        assert body["top_logprobs"] == 3
        assert body["parallel_tool_calls"] is True
        assert body["reasoning_effort"] == "high"
        assert body["service_tier"] == "flex"
        assert body["store"] is True

    @respx.mock
    def test_chat_with_advanced_json_options(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "--response-format",
                '{"type":"json_object"}',
                "--stream-options",
                '{"include_usage":true}',
                "--metadata",
                '{"team":"cli"}',
                "--logit-bias",
                '{"42":5}',
                "--modality",
                "text",
                "--modality",
                "audio",
                "--audio",
                '{"voice":"alloy","format":"mp3"}',
                "--prediction",
                '{"type":"content","content":"Hello"}',
                "--web-search-options",
                '{"search_context_size":"high"}',
                "--tools",
                '[{"type":"function","function":{"name":"lookup_weather"}}]',
                "--tool-choice",
                '{"type":"function","function":{"name":"lookup_weather"}}',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["response_format"] == {"type": "json_object"}
        assert body["stream_options"] == {"include_usage": True}
        assert body["metadata"] == {"team": "cli"}
        assert body["logit_bias"] == {"42": 5}
        assert body["modalities"] == ["text", "audio"]
        assert body["audio"] == {"voice": "alloy", "format": "mp3"}
        assert body["prediction"] == {"type": "content", "content": "Hello"}
        assert body["web_search_options"] == {"search_context_size": "high"}
        assert body["tools"] == [{"type": "function", "function": {"name": "lookup_weather"}}]
        assert body["tool_choice"] == {
            "type": "function",
            "function": {"name": "lookup_weather"},
        }

    @respx.mock
    def test_chat_with_tool_choice_enum(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--tool-choice", "required", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["tool_choice"] == "required"

    def test_chat_with_invalid_response_format_json(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "--response-format",
                "{invalid",
            ],
        )
        assert result.exit_code != 0
        assert "Invalid JSON for --response-format" in result.output

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

"""Tests for GLM CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from glm_cli.core.output import GLM_MODELS
from glm_cli.main import cli, get_version


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "glm-cli" in result.output

    def test_version_uses_distribution_name(self, monkeypatch):
        monkeypatch.setattr(
            "glm_cli.main.metadata.version",
            lambda name: "1.2.3" if name == "glm-pro-cli" else None,
        )

        assert get_version() == "1.2.3"

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_model_inventory_includes_latest_glm_model(self):
        assert GLM_MODELS[0] == "glm-5.3"


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
        result = runner.invoke(cli, ["--token", "test-token", "chat", "Hello"])
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-m", "glm-5-turbo", "--json"]
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "glm-5-turbo"

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/glm/chat/completions").mock(
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
                "You are a helpful assistant",
                "--json",
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
    def test_chat_with_openai_compatible_options(self, runner, mock_chat_response):
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
                "--max-completion-tokens",
                "512",
                "--reasoning-effort",
                "high",
                "--service-tier",
                "priority",
                "--store",
                "--logprobs",
                "--top-logprobs",
                "3",
                "--parallel-tool-calls",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["max_completion_tokens"] == 512
        assert body["reasoning_effort"] == "high"
        assert body["service_tier"] == "priority"
        assert body["store"] is True
        assert body["logprobs"] is True
        assert body["top_logprobs"] == 3
        assert body["parallel_tool_calls"] is True

    @respx.mock
    def test_chat_with_extended_openapi_options(self, runner, mock_chat_response):
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
                "--response-format",
                '{"type": "json_object"}',
                "--tools",
                '[{"type":"function","function":{"name":"lookup"}}]',
                "--tool-choice",
                "auto",
                "--stream-options",
                '{"include_usage": true}',
                "--metadata",
                '{"source": "test"}',
                "--logit-bias",
                '{"123": -1}',
                "--modalities",
                '["text"]',
                "--audio",
                '{"voice": "alloy"}',
                "--prediction",
                '{"type": "content", "content": "Hello"}',
                "--web-search-options",
                '{"search_context_size": "low"}',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["stream"] is True
        assert body["response_format"] == {"type": "json_object"}
        assert body["tools"] == [{"type": "function", "function": {"name": "lookup"}}]
        assert body["tool_choice"] == "auto"
        assert body["stream_options"] == {"include_usage": True}
        assert body["metadata"] == {"source": "test"}
        assert body["logit_bias"] == {"123": -1}
        assert body["modalities"] == ["text"]
        assert body["audio"] == {"voice": "alloy"}
        assert body["prediction"] == {"type": "content", "content": "Hello"}
        assert body["web_search_options"] == {"search_context_size": "low"}

    def test_chat_rejects_invalid_json_option(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--metadata", "not-json"],
        )
        assert result.exit_code != 0
        assert "--metadata must be valid JSON." in result.output

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "glm-5.3" in result.output
        assert "glm-5.2" in result.output
        assert "glm-5" in result.output
        assert "glm-5-turbo" in result.output
        assert "glm-4.7" in result.output
        assert "glm-5.1" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from claude_cli.core.output import CHAT_MODELS, MESSAGES_MODELS
from claude_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_model_inventory_excludes_retired_opus_3(self):
        assert CHAT_MODELS[:2] == ["claude-fable-5-1", "claude-fable-5"]
        assert "claude-opus-5" in CHAT_MODELS
        assert "claude-opus-5-5" not in CHAT_MODELS
        assert MESSAGES_MODELS[0] == "claude-opus-5-5"
        assert "claude-3-opus-20240229" not in CHAT_MODELS

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
        assert "--metadata" in result.output
        assert "Request metadata as a JSON object." in result.output
        assert "user_id" not in result.output

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

    @pytest.mark.parametrize("command", ["chat", "messages", "count-tokens"])
    def test_commands_reject_removed_model(self, runner, command):
        result = runner.invoke(
            cli,
            [command, "Hello", "--model", "claude-3-opus-20240229"],
        )
        assert result.exit_code != 0


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
                "claude-opus-5",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["model"] == "claude-opus-5"

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
    def test_chat_with_extended_openapi_options(self, runner, mock_chat_response):
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
                "--stream",
                "--response-format",
                '{"type":"json_object"}',
                "--tools",
                '[{"type":"function","function":{"name":"lookup"}}]',
                "--tool-choice",
                '{"type":"function","function":{"name":"lookup"}}',
                "--stream-options",
                '{"include_usage":true}',
                "--metadata",
                '{"source":"cli"}',
                "--modalities",
                '["text"]',
                "--web-search-options",
                '{"search_context_size":"medium"}',
                "--store",
                "--logprobs",
                "--top-logprobs",
                "3",
                "--no-parallel-tool-calls",
                "--json",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["stream"] is True
        assert request_body["response_format"] == {"type": "json_object"}
        assert request_body["tools"][0]["function"]["name"] == "lookup"
        assert request_body["tool_choice"]["function"]["name"] == "lookup"
        assert request_body["stream_options"] == {"include_usage": True}
        assert request_body["metadata"] == {"source": "cli"}
        assert request_body["modalities"] == ["text"]
        assert request_body["web_search_options"] == {"search_context_size": "medium"}
        assert request_body["store"] is True
        assert request_body["logprobs"] is True
        assert request_body["top_logprobs"] == 3
        assert request_body["parallel_tool_calls"] is False

    @respx.mock
    def test_chat_auth_error(self, runner):
        respx.post("https://api.acedata.cloud/v1/chat/completions").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        result = runner.invoke(cli, ["--token", "bad-token", "chat", "Hello"])
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
            ["--token", "test-token", "messages", "Hello", "-m", "claude-opus-5"],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["model"] == "claude-opus-5"

    @respx.mock
    def test_messages_with_extended_openapi_options(self, runner, mock_messages_response):
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
                "--metadata",
                '{"user_id":"user-1"}',
                "--stream",
                "--tools",
                '[{"name":"lookup"}]',
                "--tool-choice",
                '{"type":"auto"}',
                "--output-config",
                '{"effort":"high"}',
                "--cache-control",
                '{"type":"ephemeral","ttl":"1h"}',
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["metadata"] == {"user_id": "user-1"}
        assert request_body["stream"] is True
        assert request_body["tools"] == [{"name": "lookup"}]
        assert request_body["tool_choice"] == {"type": "auto"}
        assert request_body["output_config"] == {"effort": "high"}
        assert request_body["cache_control"] == {"type": "ephemeral", "ttl": "1h"}

    @pytest.mark.parametrize("metadata", [None, {}, {"user_id": "example-user-001"}])
    @respx.mock
    def test_messages_metadata_is_separate_from_auth_and_conversation(
        self, runner, mock_messages_response, metadata
    ):
        route = respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        options = [] if metadata is None else ["--metadata", json.dumps(metadata)]
        result = runner.invoke(
            cli, ["--token", "test-token", "messages", "Hello, Claude", *options]
        )
        assert result.exit_code == 0, result.output
        sent = route.calls[0].request
        body = json.loads(sent.content)
        assert sent.headers["authorization"] == "Bearer test-token"
        assert body["messages"] == [{"role": "user", "content": "Hello, Claude"}]
        if metadata is None:
            assert "metadata" not in body
        else:
            assert body["metadata"] == metadata

    @pytest.mark.parametrize("metadata", ["not-json", "[]", "1", '"example-user-001"'])
    @respx.mock
    def test_messages_rejects_invalid_metadata_without_request(self, runner, metadata):
        route = respx.post("https://api.acedata.cloud/v1/messages")
        result = runner.invoke(
            cli, ["--token", "test-token", "messages", "Hello", "--metadata", metadata]
        )
        assert result.exit_code != 0
        assert "--metadata" in result.output
        assert not route.called

    @respx.mock
    def test_messages_auth_error(self, runner):
        respx.post("https://api.acedata.cloud/v1/messages").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        result = runner.invoke(cli, ["--token", "bad-token", "messages", "Hello"])
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
        result = runner.invoke(cli, ["--token", "test-token", "count-tokens", "Hello world"])
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

    @respx.mock
    def test_count_tokens_with_tools(self, runner, mock_count_tokens_response):
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
                "--tools",
                '[{"name":"lookup"}]',
                "--tool-choice",
                '{"type":"auto"}',
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["tools"] == [{"name": "lookup"}]
        assert request_body["tool_choice"] == {"type": "auto"}


# ─── Models / Config Commands ────────────────────────────────────────────


class TestInfoCommands:
    """Tests for models and config commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "claude" in result.output.lower()
        assert "claude-fable-5-1" in result.output
        assert "claude-fable-5" in result.output
        assert "claude-opus-5" in result.output
        assert "claude-opus-5-5" in result.output
        assert "Messages only" in result.output

    def test_models_first_entry(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        lines = [line for line in result.output.splitlines() if "claude-" in line]
        assert "claude-opus-5-5" in lines[0]

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "API Token" in result.output
        assert "API Base URL" in result.output


# ─── Messages Thinking ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("command", "endpoint"),
    [
        ("messages", "/v1/messages"),
        ("count-tokens", "/v1/messages/count_tokens"),
    ],
)
class TestThinkingPassthrough:
    @pytest.mark.parametrize(
        ("options", "thinking"),
        [
            (["--thinking-type", "enabled"], {"type": "enabled"}),
            (
                ["--thinking-type", "enabled", "--thinking-budget-tokens", "512"],
                {"type": "enabled", "budget_tokens": 512},
            ),
            (
                ["--thinking-type", "between_tools", "--thinking-display", "updates"],
                {"type": "between_tools", "display": "updates"},
            ),
            (
                ["--thinking-type", "disabled", "--thinking-display", "summarized"],
                {"type": "disabled", "display": "summarized"},
            ),
            (["--thinking-budget-tokens", "0"], {"budget_tokens": 0}),
            (["--thinking-display", "future-display"], {"display": "future-display"}),
            (["--thinking", "{}"], {}),
        ],
    )
    @respx.mock
    def test_convenience_options(self, runner, request, command, endpoint, options, thinking):
        route = respx.post(f"https://api.acedata.cloud{endpoint}").mock(
            return_value=Response(
                200,
                json=request.getfixturevalue(
                    "mock_messages_response"
                    if command == "messages"
                    else "mock_count_tokens_response"
                ),
            )
        )
        result = runner.invoke(cli, ["--token", "test-token", command, "Hello", *options])
        assert result.exit_code == 0, result.output
        sent = route.calls[0].request
        assert json.loads(sent.content)["thinking"] == thinking
        assert "anthropic-beta" not in sent.headers

    @pytest.mark.parametrize("override", [False, True])
    @respx.mock
    def test_json_extensions_and_beta_header(self, runner, request, command, endpoint, override):
        route = respx.post(f"https://api.acedata.cloud{endpoint}").mock(
            return_value=Response(
                200,
                json=request.getfixturevalue(
                    "mock_messages_response"
                    if command == "messages"
                    else "mock_count_tokens_response"
                ),
            )
        )
        thinking = {
            "type": "between_tools",
            "display": "updates",
            "budget_tokens": 512,
            "extension": {"enabled": False, "values": [1, None]},
        }
        beta = "thinking-display-updates-2026-08-18,another-beta"
        options = ["--thinking", json.dumps(thinking), "--anthropic-beta", beta]
        if override:
            options += [
                "--thinking-type",
                "adaptive",
                "--thinking-display",
                "omitted",
                "--thinking-budget-tokens",
                "2048",
            ]
            thinking.update(type="adaptive", display="omitted", budget_tokens=2048)
        output_config = {"effort": "future-effort", "extension": {"enabled": False}}
        if command == "messages":
            options += ["--output-config", json.dumps(output_config)]
        result = runner.invoke(cli, ["--token", "test-token", command, "Hello", *options])
        assert result.exit_code == 0, result.output
        sent = route.calls[0].request
        body = json.loads(sent.content)
        assert body["thinking"] == thinking
        assert sent.headers["anthropic-beta"] == beta
        assert sent.headers["authorization"] == "Bearer test-token"
        assert "anthropic_beta" not in body
        if command == "messages":
            assert body["output_config"] == output_config

    @pytest.mark.parametrize("thinking", ["not-json", "[]", "1", '"adaptive"'])
    @respx.mock
    def test_invalid_thinking_json(self, runner, command, endpoint, thinking):
        route = respx.post(f"https://api.acedata.cloud{endpoint}")
        result = runner.invoke(
            cli, ["--token", "test-token", command, "Hello", "--thinking", thinking]
        )
        assert result.exit_code != 0
        assert "--thinking" in result.output
        assert not route.called

    @respx.mock
    def test_model_parameter_error(self, runner, command, endpoint):
        route = respx.post(f"https://api.acedata.cloud{endpoint}").mock(
            return_value=Response(400, text="Invalid thinking parameters")
        )
        result = runner.invoke(
            cli, ["--token", "test-token", command, "Hello", "--thinking-type", "enabled"]
        )
        assert result.exit_code != 0
        assert "Invalid thinking parameters" in result.output
        assert json.loads(route.calls[0].request.content)["thinking"] == {"type": "enabled"}


class TestMessagesThinking:
    """Tests for thinking configuration passthrough."""

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
                "--thinking-display",
                "summarized",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["thinking"] == {
            "type": "enabled",
            "budget_tokens": 2048,
            "display": "summarized",
        }

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
        result = runner.invoke(cli, ["--token", "test-token", "messages", "Hello"])
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body.get("thinking") is None

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
                "--thinking-display",
                "summarized",
                "--cache-control",
                '{"type":"ephemeral","ttl":"5m"}',
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["thinking"] == {
            "type": "enabled",
            "budget_tokens": 1024,
            "display": "summarized",
        }
        assert request_body["cache_control"] == {"type": "ephemeral", "ttl": "5m"}

    @respx.mock
    def test_count_tokens_without_thinking(self, runner, mock_count_tokens_response):
        route = respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
            return_value=Response(200, json=mock_count_tokens_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "count-tokens", "Hello"])
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body.get("thinking") is None

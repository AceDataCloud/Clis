"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from aichat_cli.core.output import MODELS, MODELS2
from aichat_cli.main import cli, get_version


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_model_inventory_excludes_retired_opus_3(self):
        assert "claude-fable-5-1" in MODELS2
        assert "claude-opus-5" in MODELS2
        assert "claude-3-opus-20240229" not in MODELS2

    def test_model_inventory_includes_latest_glm_models(self):
        assert "glm-5.3" in MODELS
        assert "glm-5.3" in MODELS2
        assert MODELS.count("deepseek-v4-pro") == 1
        assert MODELS2.count("deepseek-v4-pro") == 1

    def test_chat2_model_inventory_matches_gemini_models(self):
        assert "gemini-3.7-flash" in MODELS2
        assert "gemini-3.5-flash-lite" in MODELS2
        assert "gemini-2.5-pro" in MODELS2
        assert "gemini-3.1-flash-lite" in MODELS2
        assert "gemini-3.1-flash-lite-preview" not in MODELS2
        assert "gemini-3.1-pro" not in MODELS2
        assert "gemini-3-pro-preview" not in MODELS2

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "aichat-cli" in result.output

    def test_version_uses_distribution_name(self, monkeypatch):
        monkeypatch.setattr(
            "aichat_cli.main.metadata.version",
            lambda name: "1.2.3" if name == "aichat-pro-cli" else None,
        )

        assert get_version() == "1.2.3"

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "chat2" in result.output
        assert "models" in result.output
        assert "models2" in result.output
        assert "config" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "QUESTION" in result.output
        assert "--model" in result.output
        assert "--id" in result.output

    def test_help_chat2(self, runner):
        result = runner.invoke(cli, ["chat2", "--help"])
        assert result.exit_code == 0
        assert "[QUESTION]" in result.output
        assert "--model" in result.output
        assert "--action" in result.output
        assert "--model-group" in result.output
        assert "tool_use_id" in result.output
        assert "tool_call_id" not in result.output
        assert '"expires_at":1790000000' in result.output
        assert "allow_selected" not in result.output


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
            ["--token", "test-token", "chat", "Hello", "-m", "deepseek-v4-pro", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "deepseek-v4-pro"

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
        assert "gpt-5.4-mini" in result.output
        assert "gpt-5.4-nano" in result.output
        assert "glm-5.3" in result.output
        assert "glm-5" in result.output
        assert "glm-5-turbo" in result.output
        assert "gpt-4o" in result.output
        assert "deepseek" in result.output.lower()
        assert "deepseek-v4-pro" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

    def test_models2(self, runner):
        result = runner.invoke(cli, ["models2"])
        assert result.exit_code == 0
        assert "claude-opus-5" in result.output
        assert "claude-sonnet-5" in result.output
        assert "gemini-3.1-pro" in result.output
        assert "kimi-k3" in result.output
        assert "kimi-k2.6" in result.output
        assert "kimi-k2-0711-preview" not in result.output
        assert "kimi-k2-0905-preview" not in result.output
        assert "kimi-k2-instruct-0905" not in result.output
        assert "kimi-k2-turbo-preview" not in result.output
        assert "grok-4" in result.output
        assert "deepseek-v4-pro" in result.output
        assert "glm-5.3" in result.output


# ─── Chat2 Commands ──────────────────────────────────────────────────────────


class TestChat2Commands:
    """Tests for chat2 command."""

    @respx.mock
    def test_chat2_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "What is AI?", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "answer" in data
        assert "id" in data

    @respx.mock
    def test_chat2_with_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "-m", "deepseek-v4-pro", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "deepseek-v4-pro"

    @respx.mock
    def test_chat2_with_model_group(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--model-group",
                "claude",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model_group"] == "claude"

    @respx.mock
    def test_chat2_with_action(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "--action", "chat", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "chat"

    @respx.mock
    def test_chat2_with_max_turns(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "--max-turns", "5", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["max_turns"] == 5

    @respx.mock
    def test_chat2_without_question(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "--action",
                "retrieve",
                "--id",
                "abc-123",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "retrieve"
        assert body["id"] == "abc-123"
        assert "question" not in body

    @respx.mock
    def test_chat2_sends_question(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "What is the meaning of life?", "--json"],
        )
        body = json.loads(route.calls.last.request.content)
        assert body["question"] == "What is the meaning of life?"

    @respx.mock
    def test_chat2_with_no_stateful(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "--no-stateful", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["stateful"] is False

    @pytest.mark.parametrize("limit", ["0", "101", "-1"])
    def test_chat2_invalid_limit(self, runner, limit):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "--limit", limit],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_chat2_with_kimi_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "-m", "kimi-k2.6", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "kimi-k2.6"

    @pytest.mark.parametrize(
        "model",
        [
            "kimi-k2-0711-preview",
            "kimi-k2-0905-preview",
            "kimi-k2-instruct-0905",
            "kimi-k2-turbo-preview",
        ],
    )
    def test_chat2_rejects_removed_kimi_models(self, runner, model):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "-m", model],
        )
        assert result.exit_code != 0

    def test_chat2_rejects_removed_claude_model(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", "-m", "claude-3-opus-20240229"],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_chat2_with_application_id(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--application-id",
                "app-123",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["application_id"] == "app-123"

    @respx.mock
    def test_chat2_with_allowed_skills(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--allowed-skill",
                "web_search",
                "--allowed-skill",
                "code_interpreter",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["allowed_skills"] == ["web_search", "code_interpreter"]

    @respx.mock
    def test_chat2_with_allowed_mcp_servers(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--allowed-mcp-server",
                "my-server",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["allowed_mcp_servers"] == ["my-server"]

    @respx.mock
    def test_chat2_with_offset_and_limit(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--offset",
                "10",
                "--limit",
                "50",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["offset"] == 10
        assert body["limit"] == 50

    @respx.mock
    def test_chat2_with_messages(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        msgs = json.dumps([{"role": "user", "content": "Hello"}])
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--messages",
                msgs,
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["messages"] == [{"role": "user", "content": "Hello"}]

    @respx.mock
    def test_chat2_with_message(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        msg = json.dumps("Hello")
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--message",
                msg,
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["message"] == "Hello"

    @respx.mock
    def test_chat2_with_tool_results(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        tool_results = json.dumps([{"tool_use_id": "call_abc", "output": "42"}])
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--tool-results",
                tool_results,
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["tool_results"] == [{"tool_use_id": "call_abc", "output": "42"}]

    @respx.mock
    def test_chat2_with_unattended_policy(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/aichat2/conversations").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        policy = json.dumps(
            {
                "allowed_skills": ["web_search"],
                "allowed_mcp_servers": [],
                "expires_at": 1790000000,
            }
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--unattended-policy",
                policy,
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["unattended_policy"] == {
            "allowed_skills": ["web_search"],
            "allowed_mcp_servers": [],
            "expires_at": 1790000000,
        }

    def test_chat2_invalid_messages_json(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat2",
                "Hello",
                "--messages",
                "not-valid-json",
            ],
        )
        assert result.exit_code != 0

    @pytest.mark.parametrize(
        ("option", "value"),
        [
            ("--message", '{"role":"user"}'),
            ("--messages", '{"role":"user"}'),
            ("--tool-results", '[{"tool_use_id":"id"}]'),
            ("--unattended-policy", "[]"),
        ],
    )
    def test_chat2_rejects_invalid_structured_options(self, runner, option, value):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat2", "Hello", option, value],
        )
        assert result.exit_code != 0

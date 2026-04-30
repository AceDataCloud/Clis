"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from openai_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "openai-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "embed" in result.output
        assert "image" in result.output

    def test_chat_help(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_embed_help(self, runner):
        result = runner.invoke(cli, ["embed", "--help"])
        assert result.exit_code == 0
        assert "TEXT" in result.output
        assert "--model" in result.output

    def test_image_help(self, runner):
        result = runner.invoke(cli, ["image", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output

    def test_edit_help(self, runner):
        result = runner.invoke(cli, ["edit", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--image-url" in result.output

    def test_response_help(self, runner):
        result = runner.invoke(cli, ["response", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output


# ─── Chat Commands ────────────────────────────────────────────────────────


class TestChatCommands:
    """Tests for the chat command."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
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
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is the capital of France?"]
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "-m", "gpt-5.4", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-5.4"

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
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
        body = json.loads(route.calls.last.request.content)
        messages = body["messages"]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a helpful assistant"
        assert messages[1]["role"] == "user"

    @respx.mock
    def test_chat_with_temperature(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--temperature", "0.5", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["temperature"] == 0.5

    @respx.mock
    def test_chat_with_top_p(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--top-p", "0.9", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["top_p"] == 0.9

    @respx.mock
    def test_chat_with_frequency_penalty(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--frequency-penalty", "0.5", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["frequency_penalty"] == 0.5

    @respx.mock
    def test_chat_with_reasoning_effort(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--reasoning-effort", "high", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["reasoning_effort"] == "high"

    @respx.mock
    def test_chat_with_seed(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--seed", "42", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["seed"] == 42

    @respx.mock
    def test_chat_with_stop(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--stop", "END", "--stop", "STOP", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert "END" in body["stop"]
        assert "STOP" in body["stop"]

    @respx.mock
    def test_chat_with_max_completion_tokens(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--max-completion-tokens", "512", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["max_completion_tokens"] == 512

    @respx.mock
    def test_chat_with_user(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--user", "user-123", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["user"] == "user-123"

    @respx.mock
    def test_chat_with_service_tier(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--service-tier", "flex", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["service_tier"] == "flex"

    @respx.mock
    def test_chat_gpt54_model(self, runner, mock_chat_response):
        """Verify gpt-5.4 is available (restored by revert commit)."""
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "-m", "gpt-5.4", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-5.4"

    @respx.mock
    def test_chat_gpt54_pro_model(self, runner, mock_chat_response):
        """Verify gpt-5.4-pro is available."""
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "-m", "gpt-5.4-pro", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-5.4-pro"

    @respx.mock
    def test_chat_with_response_format(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
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
                '{"type": "json_object"}',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["response_format"] == {"type": "json_object"}

    @respx.mock
    def test_chat_with_invalid_response_format(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "--response-format",
                "not-json",
            ],
        )
        assert result.exit_code == 1

    @respx.mock
    def test_chat_with_logprobs(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--logprobs", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["logprobs"] is True

    @respx.mock
    def test_chat_with_top_logprobs(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--logprobs", "--top-logprobs", "5", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["top_logprobs"] == 5

    @respx.mock
    def test_chat_with_parallel_tool_calls(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--no-parallel-tool-calls", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["parallel_tool_calls"] is False

    @respx.mock
    def test_chat_with_store(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--store", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["store"] is True


# ─── Embed Commands ────────────────────────────────────────────────────────


class TestEmbedCommands:
    """Tests for the embed command."""

    @respx.mock
    def test_embed_json(self, runner, mock_embedding_response):
        respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_embedding_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "embed", "Hello world", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "data" in data

    @respx.mock
    def test_embed_with_model(self, runner, mock_embedding_response):
        route = respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_embedding_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "embed", "Hello", "-m", "text-embedding-3-large", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "text-embedding-3-large"

    @respx.mock
    def test_embed_rich_output(self, runner, mock_embedding_response):
        respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_embedding_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "embed", "Hello world"])
        assert result.exit_code == 0
        assert "Dimensions" in result.output


# ─── Image Commands ────────────────────────────────────────────────────────


class TestImageCommands:
    """Tests for image generation and editing commands."""

    @respx.mock
    def test_image_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "image", "A sunset", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "data" in data

    @respx.mock
    def test_image_rich_output(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "image", "A sunset"])
        assert result.exit_code == 0
        assert "generated-image.png" in result.output

    @respx.mock
    def test_image_with_model(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "image", "A cat", "-m", "gpt-image-1", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-image-1"

    @respx.mock
    def test_edit_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Add a rainbow",
                "--image-url",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "data" in data

    @respx.mock
    def test_edit_sends_image_url(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Add clouds",
                "--image-url",
                "https://example.com/base.png",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["image"] == "https://example.com/base.png"

    @respx.mock
    def test_edit_with_mask_url(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Add clouds",
                "--image-url",
                "https://example.com/base.png",
                "--mask-url",
                "https://example.com/mask.png",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["mask"] == "https://example.com/mask.png"

    @respx.mock
    def test_edit_with_partial_images(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Add clouds",
                "--image-url",
                "https://example.com/base.png",
                "--partial-images",
                "2",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["partial_images"] == 2

    def test_edit_requires_image_url(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "edit", "Add a rainbow"],
        )
        assert result.exit_code != 0


# ─── Response Commands ─────────────────────────────────────────────────────


class TestResponseCommands:
    """Tests for the response command."""

    @respx.mock
    def test_response_json(self, runner, mock_response_api_response):
        respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_response_api_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "response", "What is 2+2?", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "output" in data

    @respx.mock
    def test_response_rich_output(self, runner, mock_response_api_response):
        respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_response_api_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "response", "What is 2+2?"])
        assert result.exit_code == 0
        assert "42" in result.output

    @respx.mock
    def test_response_with_model(self, runner, mock_response_api_response):
        route = respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_response_api_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "response", "Hello", "-m", "gpt-5.4", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-5.4"

    @respx.mock
    def test_response_with_count(self, runner, mock_response_api_response):
        route = respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_response_api_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "response", "Hello", "-n", "2", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["n"] == 2

    @respx.mock
    def test_response_with_response_format(self, runner, mock_response_api_response):
        route = respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_response_api_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "response",
                "Hello",
                "--response-format",
                '{"type": "json_object"}',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["response_format"] == {"type": "json_object"}

    def test_response_invalid_response_format(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "response",
                "Hello",
                "--response-format",
                "not-json",
            ],
        )
        assert result.exit_code != 0




class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gpt-5.4" in result.output
        assert "gpt-4o" in result.output
        assert "text-embedding-3-small" in result.output
        assert "dall-e-3" in result.output

    def test_models_includes_gpt54(self, runner):
        """Verify gpt-5.4 is listed (restored by revert commit)."""
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gpt-5.4" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output


# ─── Tasks Commands ─────────────────────────────────────────────────────────


class TestTasksCommands:
    """Tests for the tasks command group."""

    def test_tasks_help(self, runner):
        result = runner.invoke(cli, ["tasks", "--help"])
        assert result.exit_code == 0
        assert "retrieve" in result.output
        assert "batch" in result.output

    def test_tasks_retrieve_help(self, runner):
        result = runner.invoke(cli, ["tasks", "retrieve", "--help"])
        assert result.exit_code == 0
        assert "--id" in result.output
        assert "--trace-id" in result.output

    def test_tasks_batch_help(self, runner):
        result = runner.invoke(cli, ["tasks", "batch", "--help"])
        assert result.exit_code == 0
        assert "--ids" in result.output
        assert "--trace-ids" in result.output

    def test_tasks_retrieve_requires_id_or_trace_id(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "tasks", "retrieve"])
        assert result.exit_code != 0

    @respx.mock
    def test_tasks_retrieve_by_id_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "retrieve",
                "--id",
                "7489df4c-ef03-4de0-b598-e9a590793434",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "7489df4c-ef03-4de0-b598-e9a590793434"

    @respx.mock
    def test_tasks_retrieve_by_trace_id_json(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "retrieve",
                "--trace-id",
                "my-custom-trace-001",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "retrieve"
        assert body["trace_id"] == "my-custom-trace-001"

    @respx.mock
    def test_tasks_retrieve_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "retrieve",
                "--id",
                "7489df4c-ef03-4de0-b598-e9a590793434",
            ],
        )
        assert result.exit_code == 0
        assert "7489df4c" in result.output

    @respx.mock
    def test_tasks_retrieve_empty_response(self, runner):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json={})
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "retrieve",
                "--id",
                "nonexistent-id",
            ],
        )
        assert result.exit_code == 0
        assert "No task found" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_batch_response):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_batch_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "batch",
                "--trace-ids",
                "my-trace-001",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "items" in data
        assert data["count"] == 1

    @respx.mock
    def test_tasks_batch_sends_retrieve_batch_action(self, runner, mock_task_batch_response):
        route = respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_batch_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "batch",
                "--ids",
                "id-1",
                "--ids",
                "id-2",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "retrieve_batch"
        assert "id-1" in body["ids"]
        assert "id-2" in body["ids"]

    @respx.mock
    def test_tasks_batch_rich_output(self, runner, mock_task_batch_response):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_batch_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "batch",
                "--application-id",
                "9dec7b2a-1cad-41ff-8536-d4ddaf2525d4",
            ],
        )
        assert result.exit_code == 0
        assert "Found 1 task" in result.output

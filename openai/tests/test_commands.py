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

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0

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


# ─── Info Commands ─────────────────────────────────────────────────────────


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


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task retrieval commands."""

    def test_task_help(self, runner):
        result = runner.invoke(cli, ["task", "--help"])
        assert result.exit_code == 0
        assert "--id" in result.output
        assert "--trace-id" in result.output

    def test_tasks_help(self, runner):
        result = runner.invoke(cli, ["tasks", "--help"])
        assert result.exit_code == 0
        assert "--ids" in result.output
        assert "--trace-ids" in result.output

    def test_task_requires_id_or_trace_id(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "task"])
        assert result.exit_code != 0

    @respx.mock
    def test_task_by_id_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "task",
                "--id",
                "7489df4c-ef03-4de0-b598-e9a590793434",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "7489df4c-ef03-4de0-b598-e9a590793434"

    @respx.mock
    def test_task_by_id_sends_correct_payload(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "task",
                "--id",
                "7489df4c-ef03-4de0-b598-e9a590793434",
                "--json",
            ],
        )
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "retrieve"
        assert body["id"] == "7489df4c-ef03-4de0-b598-e9a590793434"

    @respx.mock
    def test_task_by_trace_id(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "task",
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
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "task",
                "--id",
                "7489df4c-ef03-4de0-b598-e9a590793434",
            ],
        )
        assert result.exit_code == 0
        assert "7489df4c" in result.output

    @respx.mock
    def test_tasks_batch_by_ids_json(self, runner, mock_tasks_batch_response):
        respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_tasks_batch_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "--ids",
                "7489df4c-ef03-4de0-b598-e9a590793434",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "items" in data
        assert data["count"] == 1

    @respx.mock
    def test_tasks_batch_sends_correct_payload(self, runner, mock_tasks_batch_response):
        route = respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_tasks_batch_response)
        )
        runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "--trace-ids",
                "my-trace-001",
                "--trace-ids",
                "my-trace-002",
                "--json",
            ],
        )
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "retrieve_batch"
        assert "my-trace-001" in body["trace_ids"]
        assert "my-trace-002" in body["trace_ids"]

    @respx.mock
    def test_tasks_batch_with_filters(self, runner, mock_tasks_batch_response):
        route = respx.post("https://api.acedata.cloud/openai/tasks").mock(
            return_value=Response(200, json=mock_tasks_batch_response)
        )
        runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "--application-id",
                "app-123",
                "--limit",
                "5",
                "--offset",
                "10",
                "--json",
            ],
        )
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "retrieve_batch"
        assert body["application_id"] == "app-123"
        assert body["limit"] == 5
        assert body["offset"] == 10

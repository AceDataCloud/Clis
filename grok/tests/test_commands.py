"""Tests for Grok CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from grok_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "grok-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "video" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_help_video(self, runner):
        result = runner.invoke(cli, ["video", "--help"])
        assert result.exit_code == 0
        assert "--model" in result.output


class TestChatCommand:
    """Tests for chat commands."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/grok/chat/completions").mock(
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
        respx.post("https://api.acedata.cloud/grok/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "Hello"])
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/grok/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-m", "grok-3", "--json"]
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "grok-3"

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/grok/chat/completions").mock(
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
        route = respx.post("https://api.acedata.cloud/grok/chat/completions").mock(
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
        route = respx.post("https://api.acedata.cloud/grok/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--reasoning-effort", "high", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["reasoning_effort"] == "high"

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0


class TestVideoCommand:
    """Tests for video generation commands."""

    @respx.mock
    def test_video_json(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/grok/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "video", "A sunset over the ocean", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        sent = json.loads(route.calls[0].request.content)
        assert sent["prompt"] == "A sunset over the ocean"

    @respx.mock
    def test_video_rich_output(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/grok/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "video", "A sunset"]
        )
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_video_with_model(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/grok/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "video", "test",
                "-m", "grok-imagine-video-1.5-preview",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "grok-imagine-video-1.5-preview"

    @respx.mock
    def test_video_with_image_url(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/grok/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "video",
                "--image-url", "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["image_url"] == "https://example.com/photo.jpg"

    @respx.mock
    def test_video_with_aspect_ratio(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/grok/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "video", "test", "-a", "16:9", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["aspect_ratio"] == "16:9"

    @respx.mock
    def test_video_async(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/grok/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "video", "test", "--async", "--json"]
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_video_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "video", "A sunset"])
        assert result.exit_code != 0


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/grok/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "test-task-123", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "test-task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/grok/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "test-task-123"]
        )
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/grok/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "abc123", "def456", "--json"]
        )
        assert result.exit_code == 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "grok-4" in result.output
        assert "grok-3" in result.output

    def test_models_chat(self, runner):
        result = runner.invoke(cli, ["models", "--type", "chat"])
        assert result.exit_code == 0
        assert "grok-4" in result.output

    def test_models_video(self, runner):
        result = runner.invoke(cli, ["models", "--type", "video"])
        assert result.exit_code == 0
        assert "grok-imagine-video" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

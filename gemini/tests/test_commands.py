"""Tests for Gemini CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from gemini_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "gemini-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "generate" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output
        assert "--aspect-ratio" in result.output

    def test_help_image_to_video(self, runner):
        result = runner.invoke(cli, ["image-to-video", "--help"])
        assert result.exit_code == 0
        assert "--image-url" in result.output


class TestChatCommand:
    """Tests for chat commands."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
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
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "Hello"])
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-m", "gemini-2.5-pro", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_new_models(self, runner, mock_chat_response):
        for model in [
            "gemini-2.5-flash-lite",
            "gemini-3.1-flash-lite-preview",
            "gemini-3.1-flash-image",
            "gemini-2.5-flash-image",
            "gemini-3-pro-image",
        ]:
            respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
                return_value=Response(200, json=mock_chat_response)
            )
            result = runner.invoke(
                cli, ["--token", "test-token", "chat", "Hello", "-m", model, "--json"]
            )
            assert result.exit_code == 0, f"Model {model} failed: {result.output}"

    @respx.mock
    def test_chat_with_max_completion_tokens(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--max-completion-tokens", "512", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_service_tier(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--service-tier", "flex", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
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
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "--temperature", "0.5", "--json"]
        )
        assert result.exit_code == 0

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0


class TestVideoCommand:
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A sunset over the ocean", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == "task-video-123"

    @respx.mock
    def test_generate_with_aspect_ratio(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "generate", "A sunset",
                "--aspect-ratio", "9:16", "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_image_to_video(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "image-to-video", "Animate this",
                "-i", "https://example.com/photo.jpg", "--json",
            ],
        )
        assert result.exit_code == 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "A sunset"])
        assert result.exit_code != 0


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/gemini/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "task-video-123", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == "task-video-123"

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/gemini/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "task-1", "task-2", "--json"]
        )
        assert result.exit_code == 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gemini-2.5-flash" in result.output
        assert "gemini-2.5-pro" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

    def test_aspect_ratios(self, runner):
        result = runner.invoke(cli, ["aspect-ratios"])
        assert result.exit_code == 0
        assert "16:9" in result.output
        assert "9:16" in result.output

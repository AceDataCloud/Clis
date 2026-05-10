"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from fish_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "fish-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "clone-voice" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--voice-id" in result.output
        assert "--model" in result.output

    def test_help_clone_voice(self, runner):
        result = runner.invoke(cli, ["clone-voice", "--help"])
        assert result.exit_code == 0
        assert "--voice-url" in result.output


# ─── Generate Commands ─────────────────────────────────────────────────────


class TestGenerateCommands:
    """Tests for audio generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/fish/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "Hello world",
                "--voice-id",
                "d7900c21663f485ab63ebdb7e5905036",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_generate_rich_output(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/fish/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "Hello world",
                "--voice-id",
                "d7900c21663f485ab63ebdb7e5905036",
            ],
        )
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_audio_response):
        route = respx.post("https://api.acedata.cloud/fish/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "Hello world",
                "--voice-id",
                "d7900c21663f485ab63ebdb7e5905036",
                "--model",
                "fish-tts",
                "--json",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["model"] == "fish-tts"

    def test_generate_missing_voice_id(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "Hello world"],
        )
        assert result.exit_code != 0
        assert "voice-id" in result.output.lower() or "missing" in result.output.lower()

    @respx.mock
    def test_generate_api_error(self, runner):
        respx.post("https://api.acedata.cloud/fish/audios").mock(
            return_value=Response(400, json={"error": {"code": "bad_request", "message": "Invalid"}})
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "Hello world",
                "--voice-id",
                "bad-id",
                "--json",
            ],
        )
        assert result.exit_code == 1


# ─── Clone Voice Commands ──────────────────────────────────────────────────


class TestCloneVoiceCommands:
    """Tests for voice cloning commands."""

    @respx.mock
    def test_clone_voice_json(self, runner, mock_voice_response):
        respx.post("https://api.acedata.cloud/fish/voices").mock(
            return_value=Response(200, json=mock_voice_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "clone-voice",
                "--voice-url",
                "https://example.com/sample.mp3",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-voice-task-123"

    @respx.mock
    def test_clone_voice_with_title(self, runner, mock_voice_response):
        route = respx.post("https://api.acedata.cloud/fish/voices").mock(
            return_value=Response(200, json=mock_voice_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "clone-voice",
                "--voice-url",
                "https://example.com/sample.mp3",
                "--title",
                "My Voice",
                "--json",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["title"] == "My Voice"

    def test_clone_voice_missing_voice_url(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "clone-voice"],
        )
        assert result.exit_code != 0


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "task-123", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0
        assert "succeeded" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "task-123", "task-456", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_wait_completes(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "wait", "task-123", "--json"]
        )
        assert result.exit_code == 0


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "fish-tts" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "API Base URL" in result.output
        assert "Request Timeout" in result.output

"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from producer_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "producer-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output


# ─── Generate Commands ─────────────────────────────────────────────────────


class TestGenerateCommands:
    """Tests for audio generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_audio_response):
        route = respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "A test music prompt", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        body = json.loads(route.calls.last.request.content)
        assert body["prompt"] == "A test music prompt"
        assert body["lyric"] == ""

    @respx.mock
    def test_generate_rich_output(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A test prompt"]
        )
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-m", "FUZZ-2.0", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_instrumental(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--instrumental", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_lyric(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "-l",
                "[Verse]\nHello world",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_callback(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--callback-url",
                "https://example.com/callback",
                "--json",
            ],
        )
        assert result.exit_code == 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_generate_async(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "test", "--async", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_cover_json(self, runner, mock_audio_response):
        route = respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "cover", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        body = json.loads(route.calls.last.request.content)
        assert body["prompt"] == ""
        assert body["lyric"] == ""

    @respx.mock
    def test_extend_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extend", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_extend_with_continue_at(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "extend",
                "audio-abc-123",
                "--continue-at",
                "30.5",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_variation_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "variation", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_swap_vocals_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "swap-vocals", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_swap_instrumentals_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "swap-instrumentals", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_replace_section_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "replace-section",
                "audio-abc-123",
                "--replace-section-start",
                "10",
                "--replace-section-end",
                "30",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_stems_json(self, runner, mock_audio_response):
        route = respx.post("https://api.acedata.cloud/producer/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "stems", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["prompt"] == ""
        assert body["lyric"] == ""


# ─── Lyrics Commands ────────────────────────────────────────────────────────


class TestLyricsCommands:
    """Tests for lyrics generation commands."""

    @respx.mock
    def test_lyrics_json(self, runner, mock_lyrics_response):
        respx.post("https://api.acedata.cloud/producer/lyrics").mock(
            return_value=Response(200, json=mock_lyrics_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "lyrics", "A love song about the ocean", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_lyrics_rich_output(self, runner, mock_lyrics_response):
        respx.post("https://api.acedata.cloud/producer/lyrics").mock(
            return_value=Response(200, json=mock_lyrics_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "lyrics", "A test prompt"],
        )
        assert result.exit_code == 0
        assert "Test lyrics" in result.output


# ─── Media Commands ─────────────────────────────────────────────────────────


class TestMediaCommands:
    """Tests for media commands."""

    @respx.mock
    def test_upload_json(self, runner, mock_upload_response):
        respx.post("https://api.acedata.cloud/producer/upload").mock(
            return_value=Response(200, json=mock_upload_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "upload",
                "https://example.com/audio.mp3",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_video_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/videos").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "video", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_wav_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/producer/wav").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "wav", "audio-abc-123", "--json"],
        )
        assert result.exit_code == 0


# ─── Task Commands ──────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/producer/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "task-abc-123", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/producer/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "task-abc", "task-def", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_wait_completed(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/producer/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "wait", "task-abc-123", "--json"],
        )
        assert result.exit_code == 0


# ─── Info Commands ──────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "FUZZ-2.0" in result.output

    def test_actions(self, runner):
        result = runner.invoke(cli, ["actions"])
        assert result.exit_code == 0
        assert "generate" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "API Base URL" in result.output

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
        assert "tts" in result.output
        assert "voices" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_tts(self, runner):
        result = runner.invoke(cli, ["tts", "--help"])
        assert result.exit_code == 0
        assert "TEXT" in result.output
        assert "--model" in result.output
        assert "--reference-id" in result.output


# ─── TTS Commands ──────────────────────────────────────────────────────────


class TestTTSCommands:
    """Tests for text-to-speech commands."""

    @respx.mock
    def test_tts_json(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tts", "Hello, world!", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["audio_url"] == "https://cdn.example.com/test-audio.mp3"
        # Verify API payload
        sent = json.loads(route.calls[0].request.content)
        assert sent["text"] == "Hello, world!"

    @respx.mock
    def test_tts_rich_output(self, runner, mock_tts_response):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tts", "Hello"])
        assert result.exit_code == 0
        assert "cdn.example.com" in result.output

    @respx.mock
    def test_tts_with_model(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tts", "Hello", "--model", "s1", "--json"]
        )
        assert result.exit_code == 0
        # model is sent as a header, not in body
        assert route.calls[0].request.headers.get("model") == "s1"

    @respx.mock
    def test_tts_with_reference_id(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tts", "Hello", "--reference-id", "voice-123", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["reference_id"] == "voice-123"

    @respx.mock
    def test_tts_with_format(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tts", "Hello", "--format", "wav", "--json"]
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["format"] == "wav"

    @respx.mock
    def test_tts_with_callback_url_async(self, runner, mock_tts_async_response):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tts",
                "Hello",
                "--callback-url",
                "https://example.com/callback",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_tts_with_advanced_params(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tts",
                "Hello",
                "--temperature",
                "0.7",
                "--top-p",
                "0.9",
                "--repetition-penalty",
                "1.2",
                "--max-new-tokens",
                "512",
                "--latency",
                "balanced",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["temperature"] == 0.7
        assert sent["top_p"] == 0.9
        assert sent["repetition_penalty"] == 1.2
        assert sent["max_new_tokens"] == 512
        assert sent["latency"] == "balanced"

    def test_tts_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "tts", "Hello"])
        assert result.exit_code != 0


# ─── Voice Commands ────────────────────────────────────────────────────────


class TestVoiceCommands:
    """Tests for voice model commands."""

    @respx.mock
    def test_voices_json(self, runner, mock_voice_list_response):
        respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json=mock_voice_list_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "voices", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == 2
        assert len(data["items"]) == 2

    @respx.mock
    def test_voices_rich_output(self, runner, mock_voice_list_response):
        respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json=mock_voice_list_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "voices"])
        assert result.exit_code == 0
        assert "Test Voice 1" in result.output

    @respx.mock
    def test_voices_with_filters(self, runner, mock_voice_list_response):
        route = respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json=mock_voice_list_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "voices", "--language", "en", "--page-size", "20", "--json"],
        )
        assert result.exit_code == 0
        # Check query params were sent
        request = route.calls[0].request
        assert "language=en" in str(request.url)
        assert "page_size=20" in str(request.url)

    @respx.mock
    def test_voice_detail_json(self, runner, mock_voice_detail_response):
        respx.get("https://api.acedata.cloud/fish/model/voice-id-1").mock(
            return_value=Response(200, json=mock_voice_detail_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "voice", "voice-id-1", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["_id"] == "voice-id-1"

    @respx.mock
    def test_voice_detail_rich_output(self, runner, mock_voice_detail_response):
        respx.get("https://api.acedata.cloud/fish/model/voice-id-1").mock(
            return_value=Response(200, json=mock_voice_detail_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "voice", "voice-id-1"])
        assert result.exit_code == 0
        assert "Test Voice 1" in result.output


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "t-1", "t-2", "--json"]
        )
        assert result.exit_code == 0


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "s2-pro" in result.output
        assert "s1" in result.output

    def test_formats(self, runner):
        result = runner.invoke(cli, ["formats"])
        assert result.exit_code == 0
        assert "mp3" in result.output
        assert "wav" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

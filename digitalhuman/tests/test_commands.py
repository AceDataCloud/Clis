"""Tests for Digital Human CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from digitalhuman_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "digitalhuman-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "--video-url" in result.output
        assert "--audio-url" in result.output
        assert "--engine" in result.output
        assert "Supply either --video-url or --image-url." in result.output
        assert "Accepted for backward compatibility" in result.output
        assert "Output is always rendered at 720p." in result.output

    def test_help_clone_voice(self, runner):
        result = runner.invoke(cli, ["clone-voice", "--help"])
        assert result.exit_code == 0
        assert "--audio-url" in result.output
        assert "--lang" in result.output


class TestGenerateCommand:
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_video_url_json(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/digital-human/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--video-url", "https://example.com/face.mp4",
                "--audio-url", "https://example.com/speech.mp3",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "task_49af42c410c24f04ad416b28af55d237"
        sent = json.loads(route.calls[0].request.content)
        assert sent["video_url"] == "https://example.com/face.mp4"
        assert sent["audio_url"] == "https://example.com/speech.mp3"

    @respx.mock
    def test_generate_image_url(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/digital-human/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/portrait.jpg",
                "--audio-url", "https://example.com/speech.mp3",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["image_url"] == "https://example.com/portrait.jpg"

    @respx.mock
    def test_generate_with_engine(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/digital-human/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--video-url", "https://example.com/face.mp4",
                "--audio-url", "https://example.com/speech.mp3",
                "--engine", "heygem",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["engine"] == "heygem"

    @respx.mock
    def test_generate_with_text_and_voice_id(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/digital-human/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--video-url", "https://example.com/face.mp4",
                "--text", "Hello world",
                "--voice-id", "f754a190e26c",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["text"] == "Hello world"
        assert sent["voice_id"] == "f754a190e26c"

    @respx.mock
    def test_generate_async(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/digital-human/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--video-url", "https://example.com/face.mp4",
                "--audio-url", "https://example.com/speech.mp3",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_generate_with_resolution(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/digital-human/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--video-url", "https://example.com/face.mp4",
                "--audio-url", "https://example.com/speech.mp3",
                "--resolution", "540p",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["resolution"] == "540p"

    def test_generate_missing_source(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate",
             "--audio-url", "https://example.com/speech.mp3"],
        )
        assert result.exit_code != 0

    def test_generate_missing_audio(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate",
             "--video-url", "https://example.com/face.mp4"],
        )
        assert result.exit_code != 0

    def test_generate_text_without_voice_id(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate",
             "--video-url", "https://example.com/face.mp4",
             "--text", "Hello"],
        )
        assert result.exit_code != 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token", "",
                "generate",
                "--video-url", "https://example.com/face.mp4",
                "--audio-url", "https://example.com/speech.mp3",
            ],
        )
        assert result.exit_code != 0


class TestCloneVoiceCommand:
    """Tests for voice cloning commands."""

    @respx.mock
    def test_clone_voice_json(self, runner, mock_voice_response):
        route = respx.post("https://api.acedata.cloud/digital-human/voices").mock(
            return_value=Response(200, json=mock_voice_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "clone-voice",
                "--audio-url", "https://example.com/voice.wav",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["voice_id"] == "f754a190e26c"
        sent = json.loads(route.calls[0].request.content)
        assert sent["audio_url"] == "https://example.com/voice.wav"

    @respx.mock
    def test_clone_voice_with_lang(self, runner, mock_voice_response):
        route = respx.post("https://api.acedata.cloud/digital-human/voices").mock(
            return_value=Response(200, json=mock_voice_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "clone-voice",
                "--audio-url", "https://example.com/voice.wav",
                "--lang", "en",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["lang"] == "en"

    @respx.mock
    def test_clone_voice_with_name(self, runner, mock_voice_response):
        route = respx.post("https://api.acedata.cloud/digital-human/voices").mock(
            return_value=Response(200, json=mock_voice_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "clone-voice",
                "--audio-url", "https://example.com/voice.wav",
                "--name", "My Voice",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["name"] == "My Voice"

    def test_clone_voice_missing_audio_url(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "clone-voice"],
        )
        assert result.exit_code != 0


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/digital-human/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task",
             "task_49af42c410c24f04ad416b28af55d237", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "task_49af42c410c24f04ad416b28af55d237"
        sent = json.loads(route.calls[0].request.content)
        assert sent["task_id"] == "task_49af42c410c24f04ad416b28af55d237"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/digital-human/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "task_49af42c410c24f04ad416b28af55d237"],
        )
        assert result.exit_code == 0
        assert "task_49af42c410c24f04ad416b28af55d237" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/digital-human/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "task_abc123", "--json"],
        )
        assert result.exit_code == 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_engines(self, runner):
        result = runner.invoke(cli, ["engines"])
        assert result.exit_code == 0
        assert "latentsync" in result.output
        assert "heygem" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

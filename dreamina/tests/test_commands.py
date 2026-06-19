"""Tests for Dreamina CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from dreamina_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "dreamina-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "--image-url" in result.output
        assert "--audio-url" in result.output


class TestGenerateCommand:
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/dreamina/videos").mock(
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
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70"
        sent = json.loads(route.calls[0].request.content)
        assert sent["image_url"] == "https://example.com/portrait.jpg"
        assert sent["audio_url"] == "https://example.com/speech.mp3"

    @respx.mock
    def test_generate_rich_output(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/dreamina/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/portrait.jpg",
                "--audio-url", "https://example.com/speech.mp3",
            ],
        )
        assert result.exit_code == 0
        assert "0c0b4d3a" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/dreamina/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/portrait.jpg",
                "--audio-url", "https://example.com/speech.mp3",
                "-m", "omnihuman-1.5",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_prompt(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/dreamina/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/portrait.jpg",
                "--audio-url", "https://example.com/speech.mp3",
                "--prompt", "A smiling face",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["prompt"] == "A smiling face"

    @respx.mock
    def test_generate_async(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/dreamina/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/portrait.jpg",
                "--audio-url", "https://example.com/speech.mp3",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_generate_missing_required(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate"],
        )
        assert result.exit_code != 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token", "",
                "generate",
                "--image-url", "https://example.com/portrait.jpg",
                "--audio-url", "https://example.com/speech.mp3",
            ],
        )
        assert result.exit_code != 0


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/dreamina/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "362b4fed-67bd-11f1-ad11-00163e57d510", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "362b4fed-67bd-11f1-ad11-00163e57d510"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/dreamina/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "362b4fed-67bd-11f1-ad11-00163e57d510"]
        )
        assert result.exit_code == 0
        assert "362b4fed" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/dreamina/tasks").mock(
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
        assert "omnihuman-1.5" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

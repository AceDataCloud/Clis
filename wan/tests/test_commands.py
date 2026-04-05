"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from wan_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "wan-cli" in result.output

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
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A test prompt", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_generate_rich_output(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-m", "wan2.6-t2v", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_resolution(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-r", "720P", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_duration(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-d", "10", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_shot_type(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--shot-type", "single", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_callback(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
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

    @respx.mock
    def test_generate_with_audio(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--audio", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_prompt_extend(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--prompt-extend", "--json"],
        )
        assert result.exit_code == 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_image_to_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "-i",
                "https://cdn.acedata.cloud/r9vsv9.png",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_image_to_video_with_resolution(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "-i",
                "https://cdn.acedata.cloud/r9vsv9.png",
                "-r",
                "1080P",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_reference_to_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/wan/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "reference-to-video",
                "A person dancing",
                "--reference-video-urls",
                "https://example.com/ref.mp4",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/wan/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/wan/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/wan/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tasks", "t-1", "t-2", "--json"])
        assert result.exit_code == 0


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "wan2.6-t2v" in result.output
        assert "wan2.6-i2v" in result.output

    def test_resolutions(self, runner):
        result = runner.invoke(cli, ["resolutions"])
        assert result.exit_code == 0
        assert "480P" in result.output
        assert "720P" in result.output
        assert "1080P" in result.output

    def test_shot_types(self, runner):
        result = runner.invoke(cli, ["shot-types"])
        assert result.exit_code == 0
        assert "single" in result.output
        assert "multi" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from seedance_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "seedance-cli" in result.output

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
        route = respx.post("https://api.acedata.cloud/seedance/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A test prompt", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        # Verify the API payload uses the content array format
        sent = json.loads(route.calls[0].request.content)
        assert sent["content"] == [{"type": "text", "text": "A test prompt"}]
        assert "prompt" not in sent
        assert sent["ratio"] == "16:9"
        assert "aspect_ratio" not in sent

    @respx.mock
    def test_generate_rich_output(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/seedance/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/seedance/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "-m",
                "doubao-seedance-1-5-pro-251215",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_callback(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/seedance/videos").mock(
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
    def test_generate_with_new_params(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/seedance/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--seed",
                "42",
                "--watermark",
                "false",
                "--generate-audio",
                "true",
                "--return-last-frame",
                "true",
                "--service-tier",
                "flex",
                "--execution-expires-after",
                "7200",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["seed"] == 42
        assert sent["watermark"] is False
        assert sent["generate_audio"] is True
        assert sent["return_last_frame"] is True
        assert sent["service_tier"] == "flex"
        assert sent["execution_expires_after"] == 7200

    @respx.mock
    def test_generate_with_frames(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/seedance/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--frames", "29", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["frames"] == 29
        assert "duration" not in sent

    def test_generate_duration_frames_exclusive(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--duration",
                "5",
                "--frames",
                "29",
            ],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_generate_adaptive_ratio(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/seedance/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-a", "adaptive", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["ratio"] == "adaptive"

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_image_to_video_json(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/seedance/videos").mock(
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
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        # Verify the content array contains text + image_url items
        sent = json.loads(route.calls[0].request.content)
        assert {"type": "text", "text": "Animate this"} in sent["content"]
        assert {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}} in sent["content"]
        assert "image_urls" not in sent

    @respx.mock
    def test_image_to_video_multiple_images(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/seedance/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Bring to life",
                "-i",
                "https://example.com/img1.jpg",
                "-i",
                "https://example.com/img2.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        content = sent["content"]
        assert len(content) == 3  # 1 text + 2 image_url
        assert content[0] == {"type": "text", "text": "Bring to life"}
        assert content[1] == {"type": "image_url", "image_url": {"url": "https://example.com/img1.jpg"}}
        assert content[2] == {"type": "image_url", "image_url": {"url": "https://example.com/img2.jpg"}}


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/seedance/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/seedance/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/seedance/tasks").mock(
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
        assert "seedance-1-5-pro" in result.output

    def test_aspect_ratios(self, runner):
        result = runner.invoke(cli, ["aspect-ratios"])
        assert result.exit_code == 0
        assert "16:9" in result.output

    def test_resolutions(self, runner):
        result = runner.invoke(cli, ["resolutions"])
        assert result.exit_code == 0
        assert "480p" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

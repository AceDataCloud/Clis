"""Tests for CLI commands."""

import json

import respx
from click.testing import CliRunner
from httpx import Response

from hailuo_cli.main import cli


@respx.mock
def _mock_videos(response):
    return respx.post("https://api.acedata.cloud/minimax/videos").mock(
        return_value=Response(200, json=response)
    )


@respx.mock
def _mock_tasks(response):
    return respx.post("https://api.acedata.cloud/minimax/tasks").mock(
        return_value=Response(200, json=response)
    )


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "hailuo-cli" in result.output

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output


class TestGenerateCommands:
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_json(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A test prompt", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        sent = json.loads(route.calls[0].request.content)
        assert sent["prompt"] == "A test prompt"

    @respx.mock
    def test_generate_rich_output(self, mock_video_response):
        runner = CliRunner()
        respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--model", "minimax-h3", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "minimax-h3"

    @respx.mock
    def test_generate_with_image_and_audio_inputs(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "--image-url",
                "https://example.com/1.jpg",
                "--audio-url",
                "https://example.com/1.mp3",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["image_urls"] == ["https://example.com/1.jpg"]
        assert sent["audio_urls"] == ["https://example.com/1.mp3"]

    @respx.mock
    def test_generate_with_resolution_and_watermark(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "A test prompt",
                "--resolution",
                "768P",
                "--aigc-watermark",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["resolution"] == "768P"
        assert sent["aigc_watermark"] is True

    def test_generate_requires_any_input(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--token", "test-token", "generate"])
        assert result.exit_code != 0

    def test_generate_rejects_too_many_image_urls(self):
        runner = CliRunner()
        args = ["--token", "test-token", "generate", "A test prompt"]
        for i in range(10):
            args.extend(["--image-url", f"https://example.com/{i}.jpg"])
        result = runner.invoke(cli, args)
        assert result.exit_code != 0
        assert "at most 9 --image-url" in result.output

    def test_generate_rejects_too_many_audio_urls(self):
        runner = CliRunner()
        args = ["--token", "test-token", "generate", "A test prompt"]
        for i in range(4):
            args.extend(["--audio-url", f"https://example.com/{i}.mp3"])
        result = runner.invoke(cli, args)
        assert result.exit_code != 0
        assert "at most 3 --audio-url" in result.output

    def test_generate_no_token(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_image_to_video_json(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "--image-url",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        sent = json.loads(route.calls[0].request.content)
        assert sent["image_urls"] == ["https://example.com/photo.jpg"]

    @respx.mock
    def test_image_to_video_with_model(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "test",
                "--image-url",
                "https://example.com/img.jpg",
                "--model",
                "minimax-h3",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "minimax-h3"

    @respx.mock
    def test_image_to_video_with_resolution_and_watermark(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "--image-url",
                "https://example.com/photo.jpg",
                "--resolution",
                "768P",
                "--aigc-watermark",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["resolution"] == "768P"
        assert sent["aigc_watermark"] is True


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, mock_task_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        sent = json.loads(route.calls[0].request.content)
        assert sent["action"] == "retrieve"
        assert sent["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, mock_task_response):
        runner = CliRunner()
        respx.post("https://api.acedata.cloud/minimax/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, mock_tasks_batch_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/tasks").mock(
            return_value=Response(200, json=mock_tasks_batch_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tasks", "t-1", "t-2", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["action"] == "retrieve_batch"
        assert sent["ids"] == ["t-1", "t-2"]


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "minimax-h3" in result.output

    def test_config(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output


class TestImageToVideoModelChoices:
    """Tests for image-to-video model enum."""

    @respx.mock
    def test_image_to_video_with_minimax_t2v(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/minimax/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this scene",
                "--image-url",
                "https://example.com/img.jpg",
                "--model",
                "minimax-h3",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "minimax-h3"

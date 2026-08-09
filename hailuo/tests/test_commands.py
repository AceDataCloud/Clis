"""Tests for CLI commands."""

import json

import respx
from click.testing import CliRunner
from httpx import Response

from hailuo_cli.main import cli


@respx.mock
def _mock_videos(response):
    return respx.post("https://api.acedata.cloud/hailuo/videos").mock(
        return_value=Response(200, json=response)
    )


@respx.mock
def _mock_tasks(response):
    return respx.post("https://api.acedata.cloud/hailuo/tasks").mock(
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
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
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
        assert sent["action"] == "generate"
        assert sent["prompt"] == "A test prompt"
        assert sent["model"] == "minimax-t2v"

    @respx.mock
    def test_generate_rich_output(self, mock_video_response):
        runner = CliRunner()
        respx.post("https://api.acedata.cloud/hailuo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--model", "minimax-t2v", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "minimax-t2v"

    @respx.mock
    def test_generate_with_first_image(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "--first-image-url",
                "https://example.com/1.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["first_image_url"] == "https://example.com/1.jpg"

    @respx.mock
    def test_generate_async(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "A test prompt",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_generate_rejects_removed_watermark_flag(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "A test prompt", "--aigc-watermark"],
        )
        assert result.exit_code != 0
        assert "No such option" in result.output
        assert "--aigc-watermark" in result.output

    def test_generate_allows_empty_prompt(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--token", "test-token", "generate"])
        assert result.exit_code != 0

    def test_generate_rejects_long_prompt(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--token", "test-token", "generate", "a" * 7001])
        assert result.exit_code != 0
        assert "at most 7000 characters" in result.output

    def test_generate_rejects_removed_media_options(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "--image-url",
                "https://example.com/1.jpg",
                "--image-role",
                "first_frame",
                "--image-role",
                "last_frame",
            ],
        )
        assert result.exit_code != 0
        assert "No such option" in result.output

    def test_generate_no_token(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_image_to_video_json(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
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
        assert sent["action"] == "generate"
        assert sent["first_image_url"] == "https://example.com/photo.jpg"

    @respx.mock
    def test_image_to_video_with_model(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
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
                "minimax-i2v",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "minimax-i2v"

    @respx.mock
    def test_image_to_video_async(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
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
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, mock_task_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task"]["id"] == "task-123"
        sent = json.loads(route.calls[0].request.content)
        assert sent["action"] == "retrieve"
        assert sent["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, mock_task_response):
        runner = CliRunner()
        respx.post("https://api.acedata.cloud/hailuo/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, mock_tasks_batch_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/tasks").mock(
            return_value=Response(200, json=mock_tasks_batch_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tasks", "t-1", "t-2", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["action"] == "retrieve_batch"
        assert sent["ids"] == ["t-1", "t-2"]

    def test_tasks_rejects_removed_filters(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "--limit",
                "10",
                "--offset",
                "2",
                "--created-at-min",
                "100",
                "--created-at-max",
                "200",
                "--json",
            ],
        )
        assert result.exit_code != 0
        assert "No such option" in result.output

    def test_delete_is_no_longer_available(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--token", "test-token", "delete", "task-123", "--json"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "minimax-t2v" in result.output

    def test_config(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output


class TestImageToVideoModelChoices:
    """Tests for image-to-video model enum."""

    @respx.mock
    def test_image_to_video_with_minimax_i2v(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/hailuo/videos").mock(
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
                "minimax-i2v",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "minimax-i2v"

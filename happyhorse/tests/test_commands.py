"""Tests for CLI commands."""

import json

import respx
from click.testing import CliRunner
from httpx import Response

from happyhorse_cli.main import cli


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "happyhorse-cli" in result.output

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
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
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

    @respx.mock
    def test_generate_rich_output(self, mock_video_response):
        runner = CliRunner()
        respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--model",
                "happyhorse-1.0-t2v",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "happyhorse-1.0-t2v"

    @respx.mock
    def test_generate_with_resolution(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--resolution", "720P", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["resolution"] == "720P"

    @respx.mock
    def test_generate_with_ratio(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--ratio", "9:16", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["ratio"] == "9:16"

    @respx.mock
    def test_generate_with_duration(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--duration", "10", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["duration"] == 10

    @respx.mock
    def test_generate_with_seed(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--seed", "42", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["seed"] == 42

    def test_generate_no_token(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_image_to_video_json(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
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
        assert sent["image_url"] == "https://example.com/photo.jpg"
        assert sent["action"] == "image_to_video"

    @respx.mock
    def test_image_to_video_with_model(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
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
                "happyhorse-1.0-i2v",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["model"] == "happyhorse-1.0-i2v"

    @respx.mock
    def test_reference_to_video_json(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "reference-to-video",
                "Create scene",
                "--image-urls",
                "https://example.com/ref1.jpg",
                "--image-urls",
                "https://example.com/ref2.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        sent = json.loads(route.calls[0].request.content)
        assert sent["action"] == "reference_to_video"
        assert sent["image_urls"] == [
            "https://example.com/ref1.jpg",
            "https://example.com/ref2.jpg",
        ]

    @respx.mock
    def test_video_edit_json(self, mock_video_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "video-edit",
                "Add music",
                "--video-url",
                "https://example.com/video.mp4",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        sent = json.loads(route.calls[0].request.content)
        assert sent["action"] == "video_edit"
        assert sent["video_url"] == "https://example.com/video.mp4"


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, mock_task_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/tasks").mock(
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
        respx.post("https://api.acedata.cloud/happyhorse/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, mock_tasks_batch_response):
        runner = CliRunner()
        route = respx.post("https://api.acedata.cloud/happyhorse/tasks").mock(
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
        assert "happyhorse-1.1-t2v" in result.output

    def test_config(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

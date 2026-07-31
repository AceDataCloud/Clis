"""Tests for DrawAI CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from drawai_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "drawai-cli" in result.output

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
        assert "--template" in result.output
        assert "--mode" in result.output


class TestGenerateCommand:
    """Tests for headshot generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_headshot_response):
        route = respx.post("https://api.acedata.cloud/headshots/generate").mock(
            return_value=Response(200, json=mock_headshot_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/face.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "abc123-def456"
        sent = json.loads(route.calls[0].request.content)
        assert "https://example.com/face.jpg" in sent["image_urls"]

    @respx.mock
    def test_generate_with_template(self, runner, mock_headshot_response):
        route = respx.post("https://api.acedata.cloud/headshots/generate").mock(
            return_value=Response(200, json=mock_headshot_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/face.jpg",
                "--template", "wedding",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["template"] == "wedding"

    @respx.mock
    def test_generate_with_mode(self, runner, mock_headshot_response):
        route = respx.post("https://api.acedata.cloud/headshots/generate").mock(
            return_value=Response(200, json=mock_headshot_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/face.jpg",
                "--mode", "relax",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["mode"] == "relax"

    @respx.mock
    def test_generate_async(self, runner, mock_headshot_response):
        route = respx.post("https://api.acedata.cloud/headshots/generate").mock(
            return_value=Response(200, json=mock_headshot_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/face.jpg",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_generate_multiple_images(self, runner, mock_headshot_response):
        route = respx.post("https://api.acedata.cloud/headshots/generate").mock(
            return_value=Response(200, json=mock_headshot_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/face1.jpg",
                "--image-url", "https://example.com/face2.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert len(sent["image_urls"]) == 2

    @respx.mock
    def test_generate_rich_output(self, runner, mock_headshot_response):
        respx.post("https://api.acedata.cloud/headshots/generate").mock(
            return_value=Response(200, json=mock_headshot_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "--image-url", "https://example.com/face.jpg",
            ],
        )
        assert result.exit_code == 0
        assert "abc123-def456" in result.output

    def test_generate_missing_image_url(self, runner):
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
                "--image-url", "https://example.com/face.jpg",
            ],
        )
        assert result.exit_code != 0


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/headshots/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "abc123-def456", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "abc123-def456"
        sent = json.loads(route.calls[0].request.content)
        assert sent["id"] == "abc123-def456"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/headshots/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "abc123-def456"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/headshots/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "abc123", "def456", "--json"]
        )
        assert result.exit_code == 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_templates(self, runner):
        result = runner.invoke(cli, ["templates"])
        assert result.exit_code == 0
        assert "business_photo" in result.output
        assert "wedding" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

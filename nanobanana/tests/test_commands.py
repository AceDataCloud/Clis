"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from nanobanana_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "nano-banana-pro-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "edit" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output
        assert "--aspect-ratio" in result.output

    def test_help_edit(self, runner):
        result = runner.invoke(cli, ["edit", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--image-url" in result.output
        assert "--model" in result.output


# ─── Image Commands ────────────────────────────────────────────────────────


class TestImageCommands:
    """Tests for image generation and editing commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A beautiful sunset", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_generate_rich_output(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A beautiful sunset"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-m", "nano-banana-pro", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_aspect_ratio(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-a", "16:9", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_resolution(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "-m",
                "nano-banana-pro",
                "-r",
                "4K",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_callback(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
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
    def test_edit_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Make it blue",
                "-i",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_edit_multiple_images(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Combine these images",
                "-i",
                "https://example.com/a.jpg",
                "-i",
                "https://example.com/b.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_edit_with_model(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Style transfer",
                "-i",
                "https://example.com/photo.jpg",
                "-m",
                "nano-banana-pro",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_edit_rich_output(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/nano-banana/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Make it artistic",
                "-i",
                "https://example.com/photo.jpg",
            ],
        )
        assert result.exit_code == 0
        assert "test-task-123" in result.output


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/nano-banana/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/nano-banana/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/nano-banana/tasks").mock(
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
        assert "nano-banana" in result.output
        assert "nano-banana-pro" in result.output

    def test_aspect_ratios(self, runner):
        result = runner.invoke(cli, ["aspect-ratios"])
        assert result.exit_code == 0
        assert "1:1" in result.output
        assert "16:9" in result.output
        assert "9:16" in result.output

    def test_resolutions(self, runner):
        result = runner.invoke(cli, ["resolutions"])
        assert result.exit_code == 0
        assert "1K" in result.output
        assert "4K" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

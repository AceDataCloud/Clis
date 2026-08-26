"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from qwen_image_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "qwen-image-cli" in result.output

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
        assert "--size" in result.output
        assert "--prompt-extend-mode" in result.output

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
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A beautiful sunset"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-m", "qwen-image-3.0", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_pro_model(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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
                "qwen-image-3.0-pro",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_size(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--size", "1024*1536", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_prompt_options(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--prompt-extend-mode",
                "agent",
                "--no-enable-thinking",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_callback(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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

    @respx.mock
    def test_generate_with_count(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-n", "3", "--json"],
        )
        assert result.exit_code == 0

    def test_generate_n_out_of_range(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-n", "7"],
        )
        assert result.exit_code != 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_edit_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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

    @respx.mock
    def test_edit_with_output_options(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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
                "--size",
                "1024*1536",
                "--prompt-extend-mode",
                "agent",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["size"] == "1024*1536"
        assert body["prompt_extend_mode"] == "agent"
        assert body["image_urls"] == ["https://example.com/photo.jpg"]
        data = json.loads(result.output)
        assert data["success"] is True

    def test_edit_requires_image_url(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "edit", "Make it blue", "--json"])
        assert result.exit_code != 0
        assert "Missing option" in result.output

    @respx.mock
    def test_wait_handles_top_level_task_response(self, runner):
        respx.post("https://api.acedata.cloud/qwen-image/tasks").mock(
            return_value=Response(200, json={"id": "task-123", "state": "completed"})
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "wait", "task-123", "--interval", "0"]
        )
        assert result.exit_code == 0
        assert "completed" in result.output

    def test_edit_rejects_more_than_three_images(self, runner):
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
                "-i",
                "https://example.com/c.jpg",
                "-i",
                "https://example.com/d.jpg",
                "--json",
            ],
        )
        assert result.exit_code != 0
        assert "maximum of 3 image URLs" in result.output

    @respx.mock
    def test_edit_multiple_images(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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
                "qwen-image-3.0-pro",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_edit_rich_output(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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

    @respx.mock
    def test_edit_with_count(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/qwen-image/images").mock(
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
                "-n",
                "2",
                "--json",
            ],
        )
        assert result.exit_code == 0


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/qwen-image/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/qwen-image/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/qwen-image/tasks").mock(
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
        assert "qwen-image-3.0" in result.output
        assert "qwen-image-3.0-pro" in result.output

    def test_prompt_extend_modes(self, runner):
        result = runner.invoke(cli, ["prompt-extend-modes"])
        assert result.exit_code == 0
        assert "direct" in result.output
        assert "agent" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

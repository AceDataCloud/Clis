"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from seedream_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "seedream-cli" in result.output

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
    """Tests for image generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A test prompt", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_generate_rich_output(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
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
                "doubao-seedream-4-5-251128",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_callback(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
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
    def test_generate_with_seed(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--seed", "42", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert json.loads(route.calls[0].request.content)["seed"] == 42

    @respx.mock
    def test_generate_with_guidance_scale(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--guidance-scale", "3.5", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert json.loads(route.calls[0].request.content)["guidance_scale"] == 3.5

    @respx.mock
    def test_generate_with_watermark_disabled(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--no-watermark", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert json.loads(route.calls[0].request.content)["watermark"] is False

    @respx.mock
    def test_generate_with_response_format(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--response-format", "b64_json", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert json.loads(route.calls[0].request.content)["response_format"] == "b64_json"

    @respx.mock
    def test_generate_with_sequential_image_generation(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--sequential-image-generation", "auto", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert json.loads(route.calls[0].request.content)["sequential_image_generation"] == "auto"

    @respx.mock
    def test_generate_with_stream(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--stream", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert json.loads(route.calls[0].request.content)["stream"] is True

    @respx.mock
    def test_generate_with_output_format(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--output-format", "png", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert json.loads(route.calls[0].request.content)["output_format"] == "png"

    @respx.mock
    def test_generate_with_web_search(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--web-search", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        body = json.loads(route.calls[0].request.content)
        assert body["tools"] == [{"type": "web_search"}]

    @respx.mock
    def test_edit_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/seedream/images").mock(
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
        respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "Combine",
                "-i",
                "https://example.com/a.jpg",
                "-i",
                "https://example.com/b.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_edit_uses_image_key(self, runner, mock_image_response):
        """Verify edit command sends 'image' (not 'image_urls') and no 'action' field."""
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
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
        body = json.loads(route.calls[0].request.content)
        assert "image" in body
        assert body["image"] == ["https://example.com/photo.jpg"]
        assert "image_urls" not in body
        assert "action" not in body

    @respx.mock
    def test_edit_with_seed_and_guidance(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
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
                "--seed",
                "123",
                "--guidance-scale",
                "5.5",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls[0].request.content)
        assert body["seed"] == 123
        assert body["guidance_scale"] == 5.5


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/seedream/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/seedream/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/seedream/tasks").mock(
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
        assert "doubao-seedream-4-5-251128" in result.output

    def test_resolutions(self, runner):
        result = runner.invoke(cli, ["resolutions"])
        assert result.exit_code == 0
        assert "1K" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

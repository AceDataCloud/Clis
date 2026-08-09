"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from veo_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "veo-cli" in result.output

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

    def test_help_task_options(self, runner):
        result = runner.invoke(cli, ["tasks", "--help"])
        assert result.exit_code == 0
        assert "--trace-ids" in result.output
        assert "--created-at-max" in result.output


# ─── Generate Commands ─────────────────────────────────────────────────────


class TestGenerateCommands:
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
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
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-m", "veo3", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_veo31_fast_ingredient(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-m", "veo31-fast-ingredients", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_portrait_aspect_ratio(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-a", "9:16", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_callback(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
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

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_generate_with_resolution(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "-r", "4k", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_translation(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--translation", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_image_to_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
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

    @respx.mock
    def test_image_to_video_with_resolution(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
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
                "-r",
                "1080p",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_ingredients_to_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "ingredients-to-video",
                "Product showcase",
                "-i",
                "https://example.com/product.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_ingredients_to_video_multiple_images(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "ingredients-to-video",
                "Scene",
                "-i",
                "https://example.com/img1.jpg",
                "-i",
                "https://example.com/img2.jpg",
                "-i",
                "https://example.com/img3.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_ingredients_to_video_with_translation(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "ingredients-to-video",
                "产品展示",
                "-i",
                "https://example.com/product.jpg",
                "--translation",
                "--json",
            ],
        )
        assert result.exit_code == 0

    def test_ingredients_to_video_requires_image(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "ingredients-to-video", "Scene"],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_upscale_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "upscale", "video-123", "--json"],
        )
        assert result.exit_code == 0
        assert respx.calls.last is not None
        payload = json.loads(respx.calls.last.request.read().decode("utf-8"))
        assert payload["action"] == "get1080p"


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/veo/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_with_trace_id(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/veo/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "--trace-id", "trace-123", "--json"],
        )
        assert result.exit_code == 0
        assert respx.calls.last is not None
        payload = json.loads(respx.calls.last.request.read().decode("utf-8"))
        assert payload["action"] == "retrieve"
        assert payload["trace_id"] == "trace-123"
        assert "id" not in payload

    def test_task_requires_id_or_trace_id(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "task"])
        assert result.exit_code != 0
        assert "Provide TASK_ID or --trace-id" in result.output

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/veo/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/veo/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tasks", "t-1", "t-2", "--json"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch_with_trace_ids_and_filters(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/veo/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "--trace-ids",
                "trace-1",
                "--trace-ids",
                "trace-2",
                "--offset",
                "2",
                "--limit",
                "10",
                "--type",
                "videos",
                "--created-at-min",
                "100.5",
                "--created-at-max",
                "200.5",
                "--json",
            ],
        )
        assert result.exit_code == 0
        assert respx.calls.last is not None
        payload = json.loads(respx.calls.last.request.read().decode("utf-8"))
        assert payload == {
            "trace_ids": ["trace-1", "trace-2"],
            "offset": 2,
            "limit": 10,
            "type": "videos",
            "created_at_min": 100.5,
            "created_at_max": 200.5,
            "action": "retrieve_batch",
        }

    @respx.mock
    def test_wait_accepts_trace_id_and_single_task_response(self, runner):
        respx.post("https://api.acedata.cloud/veo/tasks").mock(
            return_value=Response(
                200,
                json={
                    "id": "task-123",
                    "trace_id": "trace-123",
                    "type": "videos",
                    "state": "succeeded",
                    "created_at": 1786281000.1,
                },
            )
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "wait", "--trace-id", "trace-123", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "task-123"
        assert respx.calls.last is not None
        payload = json.loads(respx.calls.last.request.read().decode("utf-8"))
        assert payload["trace_id"] == "trace-123"
        assert "id" not in payload


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "veo3" in result.output
        assert "veo31-fast-ingredients" in result.output

    def test_aspect_ratios(self, runner):
        result = runner.invoke(cli, ["aspect-ratios"])
        assert result.exit_code == 0
        assert "16:9" in result.output
        assert "9:16" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

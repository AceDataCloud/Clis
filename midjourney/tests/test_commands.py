"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from midjourney_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "midjourney-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "imagine" in result.output
        assert "transform" in result.output
        assert "edit" in result.output
        assert "task" in result.output

    def test_help_imagine(self, runner):
        result = runner.invoke(cli, ["imagine", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--mode" in result.output


# ─── Imagine Commands ─────────────────────────────────────────────────────


class TestImagineCommands:
    """Tests for image generation commands."""

    @respx.mock
    def test_imagine_json(self, runner, mock_imagine_response):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "imagine", "A test prompt", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_imagine_rich_output(self, runner, mock_imagine_response):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "imagine", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_imagine_with_mode(self, runner, mock_imagine_response):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--mode", "turbo", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_imagine_with_version(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--version", "8", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["version"] == "8"

    @respx.mock
    def test_imagine_with_hd(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--hd", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["hd"] is True

    @respx.mock
    def test_imagine_with_translation(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--translation", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["translation"] is True

    @respx.mock
    def test_imagine_with_style_reference(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--style-reference", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["style_reference"] is True

    @respx.mock
    def test_imagine_with_moodboard(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--moodboard", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["moodboard"] is True

    @respx.mock
    def test_imagine_no_style_reference_by_default(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert "style_reference" not in body
        assert "moodboard" not in body

    def test_imagine_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "imagine", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_transform_json(self, runner, mock_imagine_response):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "transform", "img-123", "upscale1", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_blend_json(self, runner, mock_imagine_response):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "blend",
                "https://example.com/img1.jpg",
                "https://example.com/img2.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0


# ─── Edit Commands ────────────────────────────────────────────────────────


class TestEditCommands:
    """Tests for edit and describe commands."""

    @respx.mock
    def test_edit_json(self, runner, mock_edit_response):
        respx.post("https://api.acedata.cloud/midjourney/edits").mock(
            return_value=Response(200, json=mock_edit_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit",
                "https://example.com/img.jpg",
                "Add sunset",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_describe_json(self, runner, mock_describe_response):
        respx.post("https://api.acedata.cloud/midjourney/describe").mock(
            return_value=Response(200, json=mock_describe_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "describe", "https://example.com/img.jpg", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["descriptions"]) == 4

    @respx.mock
    def test_translate_json(self, runner, mock_translate_response):
        respx.post("https://api.acedata.cloud/midjourney/translate").mock(
            return_value=Response(200, json=mock_translate_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "translate", "一只猫", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["translated_content"] == "A cat sitting on a table"


# ─── Video Commands ───────────────────────────────────────────────────────


class TestVideoCommands:
    """Tests for video generation commands."""

    @respx.mock
    def test_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/midjourney/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "video",
                "A cat walking",
                "--image-url",
                "https://example.com/cat.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert len(data["video_urls"]) == 2

    @respx.mock
    def test_extend_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/midjourney/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "extend-video",
                "vid-123",
                "Continue the action",
                "--json",
            ],
        )
        assert result.exit_code == 0


# ─── Task Commands ────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["image_url"] == "https://cdn.example.com/result.png"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tasks", "t-1", "t-2", "--json"])
        assert result.exit_code == 0

    @respx.mock
    def test_task_with_trace_id(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "--trace-id", "trace-xyz", "--json"]
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["trace_id"] == "trace-xyz"
        assert body["action"] == "retrieve"

    @respx.mock
    def test_tasks_batch_with_trace_ids(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
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
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "retrieve_batch"
        assert body["trace_ids"] == ["trace-1", "trace-2"]

    @respx.mock
    def test_tasks_batch_with_pagination(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "t-1",
                "t-2",
                "--offset",
                "0",
                "--limit",
                "10",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["offset"] == 0
        assert body["limit"] == 10

    def test_task_no_id_no_trace_id(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "task"])
        assert result.exit_code != 0

    def test_tasks_no_ids_no_trace_ids(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "tasks"])
        assert result.exit_code != 0

    @respx.mock
    def test_seed_json(self, runner, mock_seed_response):
        respx.post("https://api.acedata.cloud/midjourney/seed").mock(
            return_value=Response(200, json=mock_seed_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "seed", "img-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["seed"] == 1234567890


# ─── Info Commands ────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_modes(self, runner):
        result = runner.invoke(cli, ["modes"])
        assert result.exit_code == 0
        assert "fast" in result.output

    def test_versions(self, runner):
        result = runner.invoke(cli, ["versions"])
        assert result.exit_code == 0
        assert "8" in result.output

    def test_actions(self, runner):
        result = runner.invoke(cli, ["actions"])
        assert result.exit_code == 0
        assert "upscale" in result.output.lower()

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

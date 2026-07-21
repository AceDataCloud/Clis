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
        assert "edits" in result.output
        assert "videos" in result.output
        assert "describe" in result.output
        assert "shorten" in result.output
        assert "translate" in result.output
        assert "seed" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_imagine(self, runner):
        result = runner.invoke(cli, ["imagine", "--help"])
        assert result.exit_code == 0
        assert "--mode" in result.output

    def test_help_edits(self, runner):
        result = runner.invoke(cli, ["edits", "--help"])
        assert result.exit_code == 0
        assert "--image-url" in result.output
        assert "--prompt" in result.output

    def test_help_videos(self, runner):
        result = runner.invoke(cli, ["videos", "--help"])
        assert result.exit_code == 0
        assert "--action" in result.output
        assert "--resolution" in result.output

    def test_help_describe(self, runner):
        result = runner.invoke(cli, ["describe", "--help"])
        assert result.exit_code == 0
        assert "--image-url" in result.output

    def test_help_shorten(self, runner):
        result = runner.invoke(cli, ["shorten", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output

    def test_help_translate(self, runner):
        result = runner.invoke(cli, ["translate", "--help"])
        assert result.exit_code == 0
        assert "CONTENT" in result.output

    def test_help_seed(self, runner):
        result = runner.invoke(cli, ["seed", "--help"])
        assert result.exit_code == 0
        assert "--image-id" in result.output

    def test_help_task(self, runner):
        result = runner.invoke(cli, ["task", "--help"])
        assert result.exit_code == 0
        assert "TASK_ID" in result.output

    def test_help_tasks(self, runner):
        result = runner.invoke(cli, ["tasks", "--help"])
        assert result.exit_code == 0

    def test_help_wait(self, runner):
        result = runner.invoke(cli, ["wait", "--help"])
        assert result.exit_code == 0
        assert "--interval" in result.output
        assert "--timeout" in result.output

    def test_help_config(self, runner):
        result = runner.invoke(cli, ["config", "--help"])
        assert result.exit_code == 0


# ─── Imagine Commands ──────────────────────────────────────────────────────


class TestImagineCommand:
    """Tests for the imagine command."""

    @respx.mock
    def test_imagine_json(self, runner, mock_imagine_response):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "imagine", "A test prompt", "--json"]
        )
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
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--mode", "turbo", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["mode"] == "turbo"

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
    def test_imagine_with_callback(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "imagine",
                "test",
                "--callback-url",
                "https://example.com/callback",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["callback_url"] == "https://example.com/callback"

    @respx.mock
    def test_imagine_with_version(self, runner, mock_imagine_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_imagine_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "test", "--version", "6.1", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["version"] == "6.1"

    def test_imagine_no_token(self, runner):
        result = runner.invoke(cli, ["imagine", "test"])
        assert result.exit_code != 0 or "Error" in result.output or "token" in result.output.lower()

    @respx.mock
    def test_imagine_api_error(self, runner):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(400, json={"error": "bad request"})
        )
        result = runner.invoke(cli, ["--token", "test-token", "imagine", "test"])
        assert result.exit_code != 0 or "Error" in result.output


# ─── Edits Commands ────────────────────────────────────────────────────────


class TestEditsCommand:
    """Tests for the edits command."""

    @respx.mock
    def test_edits_json(self, runner, mock_edits_response):
        respx.post("https://api.acedata.cloud/midjourney/edits").mock(
            return_value=Response(200, json=mock_edits_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edits",
                "--image-url",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_edits_with_prompt(self, runner, mock_edits_response):
        route = respx.post("https://api.acedata.cloud/midjourney/edits").mock(
            return_value=Response(200, json=mock_edits_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edits",
                "--image-url",
                "https://example.com/photo.jpg",
                "--prompt",
                "Add mountains",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["prompt"] == "Add mountains"

    @respx.mock
    def test_edits_with_mode(self, runner, mock_edits_response):
        route = respx.post("https://api.acedata.cloud/midjourney/edits").mock(
            return_value=Response(200, json=mock_edits_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edits",
                "--image-url",
                "https://example.com/photo.jpg",
                "--mode",
                "fast",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["mode"] == "fast"


# ─── Videos Commands ───────────────────────────────────────────────────────


class TestVideosCommand:
    """Tests for the videos command."""

    @respx.mock
    def test_videos_json(self, runner, mock_videos_response):
        respx.post("https://api.acedata.cloud/midjourney/videos").mock(
            return_value=Response(200, json=mock_videos_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "videos",
                "--prompt",
                "A flowing river",
                "--action",
                "generate",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_videos_with_resolution(self, runner, mock_videos_response):
        route = respx.post("https://api.acedata.cloud/midjourney/videos").mock(
            return_value=Response(200, json=mock_videos_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "videos",
                "--action",
                "generate",
                "--resolution",
                "720p",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["resolution"] == "720p"

    @respx.mock
    def test_videos_extend(self, runner, mock_videos_response):
        route = respx.post("https://api.acedata.cloud/midjourney/videos").mock(
            return_value=Response(200, json=mock_videos_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "videos",
                "--action",
                "extend",
                "--video-id",
                "video-abc123",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "extend"
        assert body["video_id"] == "video-abc123"


# ─── Utility Commands ──────────────────────────────────────────────────────


class TestUtilityCommands:
    """Tests for describe, shorten, translate, and seed commands."""

    @respx.mock
    def test_describe_json(self, runner, mock_describe_response):
        respx.post("https://api.acedata.cloud/midjourney/describe").mock(
            return_value=Response(200, json=mock_describe_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "describe",
                "--image-url",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_describe_missing_image_url(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "describe"])
        assert result.exit_code != 0

    @respx.mock
    def test_shorten_json(self, runner, mock_shorten_response):
        respx.post("https://api.acedata.cloud/midjourney/shorten").mock(
            return_value=Response(200, json=mock_shorten_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "shorten", "A very long prompt", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_translate_json(self, runner, mock_translate_response):
        respx.post("https://api.acedata.cloud/midjourney/translate").mock(
            return_value=Response(200, json=mock_translate_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "translate", "Una hermosa puesta de sol", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_seed_json(self, runner, mock_seed_response):
        respx.post("https://api.acedata.cloud/midjourney/seed").mock(
            return_value=Response(200, json=mock_seed_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "seed", "--image-id", "abc123", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_seed_missing_image_id(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "seed"])
        assert result.exit_code != 0


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "abc123-def456", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "abc123-def456"])
        assert result.exit_code == 0
        assert "task-123" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "abc123", "def456", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_task_request_payload(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "abc123-def456", "--json"]
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["id"] == "abc123-def456"
        assert body["action"] == "retrieve"

    @respx.mock
    def test_tasks_batch_request_payload(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "abc123", "def456", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["ids"] == ["abc123", "def456"]
        assert body["action"] == "retrieve_batch"

    @respx.mock
    def test_wait_completes(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "wait", "abc123-def456", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_wait_timeout(self, runner):
        respx.post("https://api.acedata.cloud/midjourney/tasks").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": [{"id": "task-123", "state": "pending"}],
                },
            )
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "wait",
                "abc123",
                "--interval",
                "1",
                "--timeout",
                "1",
            ],
        )
        assert result.exit_code != 0


# ─── Auth / Error ──────────────────────────────────────────────────────────


class TestErrorHandling:
    """Tests for error handling."""

    @respx.mock
    def test_auth_error_401(self, runner):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )
        result = runner.invoke(cli, ["--token", "bad-token", "imagine", "test"])
        assert result.exit_code != 0
        assert "Error" in result.output or "token" in result.output.lower()

    @respx.mock
    def test_api_error_400(self, runner):
        respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(400, json={"error": "bad request"})
        )
        result = runner.invoke(cli, ["--token", "test-token", "imagine", "test"])
        assert result.exit_code != 0 or "Error" in result.output

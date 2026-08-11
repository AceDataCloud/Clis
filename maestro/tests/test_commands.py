"""Tests for Maestro CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from maestro_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Help ──────────────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "create" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_create(self, runner):
        result = runner.invoke(cli, ["create", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--action" in result.output

    def test_help_task(self, runner):
        result = runner.invoke(cli, ["task", "--help"])
        assert result.exit_code == 0
        assert "TASK_ID" in result.output

    def test_help_wait(self, runner):
        result = runner.invoke(cli, ["wait", "--help"])
        assert result.exit_code == 0
        assert "TASK_ID" in result.output


# ─── Create Commands ───────────────────────────────────────────────────────


class TestCreateCommand:
    """Tests for the create command."""

    @respx.mock
    def test_create_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "create", "A product demo video", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "maestro-task-123"

    @respx.mock
    def test_create_rich_output(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "create", "A product demo video"])
        assert result.exit_code == 0
        assert "maestro-task-123" in result.output

    @respx.mock
    def test_create_with_aspect_ratio(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--aspect",
                "16:9",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_with_quality(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--quality",
                "pro",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["quality"] == "pro"

    @respx.mock
    def test_create_with_scenario(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--scenario",
                "narrated",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_with_captions_scenario(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--scenario",
                "captions",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["scenario"] == "captions"

    @respx.mock
    def test_sku_limits_fail_before_api_call(self, runner):
        route = respx.post("https://api.acedata.cloud/maestro/videos")
        lite = runner.invoke(
            cli,
            ["--token", "test-token", "create", "test", "--quality", "lite", "--duration", "31"],
        )
        drama = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--quality",
                "standard",
                "--scenario",
                "drama",
            ],
        )
        assert lite.exit_code != 0 and "at most 30 seconds" in lite.output
        assert drama.exit_code != 0 and "higher Maestro SKU" in drama.output
        assert not route.called

    @respx.mock
    def test_create_with_style(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--style",
                "cinematic",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_with_custom_style(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--style",
                "my-custom-style",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["style"] == "my-custom-style"

    @respx.mock
    def test_create_with_voice(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--voice",
                "warm-female",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_with_custom_voice_reference_id(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        voice_id = "1234567890abcdef1234567890abcdef"
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--voice",
                voice_id,
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["voice"] == voice_id

    @respx.mock
    def test_create_with_duration(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--duration",
                "60",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_extend_with_ref_task_id(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "continue the story",
                "--action",
                "extend",
                "--quality",
                "pro",
                "--ref-task-id",
                "prev-task-id",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_with_multiple_langs(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--lang",
                "zh-cn",
                "--lang",
                "en",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["langs"] == ["zh-cn", "en"]

    @respx.mock
    def test_create_with_file_urls(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--file-url",
                "https://example.com/img.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_with_callback_url(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--callback-url",
                "https://hooks.example.com/maestro",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_create_invalid_action(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--action",
                "invalid-action",
            ],
        )
        assert result.exit_code != 0

    @pytest.mark.parametrize("duration", ["4", "301"])
    def test_create_rejects_duration_outside_api_range(self, runner, duration):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "create", "test", "--duration", duration],
        )
        assert result.exit_code != 0

    def test_create_requires_ref_task_id_for_non_generate_action(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "create", "test", "--action", "edit"],
        )
        assert result.exit_code != 0
        assert "--ref-task-id is required" in result.output

    def test_create_rejects_more_than_four_languages(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "create",
                "test",
                "--lang",
                "zh-cn",
                "--lang",
                "en",
                "--lang",
                "es",
                "--lang",
                "fr",
                "--lang",
                "de",
            ],
        )
        assert result.exit_code != 0
        assert "standard supports at most 2 language(s)" in result.output

    @respx.mock
    def test_create_api_error(self, runner, mock_error_response):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(400, json=mock_error_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "create", "test", "--json"],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_create_auth_error(self, runner):
        respx.post("https://api.acedata.cloud/maestro/videos").mock(
            return_value=Response(401, json={"detail": "Unauthorized"})
        )
        result = runner.invoke(
            cli,
            ["--token", "bad-token", "create", "test", "--json"],
        )
        assert result.exit_code != 0


# ─── Task Command ─────────────────────────────────────────────────────────


class TestTaskCommand:
    """Tests for the task command."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/maestro/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "maestro-task-123", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "maestro-task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/maestro/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "maestro-task-123"],
        )
        assert result.exit_code == 0
        assert "maestro-task-123" in result.output

    @respx.mock
    def test_task_api_error(self, runner, mock_error_response):
        respx.post("https://api.acedata.cloud/maestro/tasks").mock(
            return_value=Response(400, json=mock_error_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "bad-task-id"],
        )
        assert result.exit_code != 0


# ─── Wait Command ─────────────────────────────────────────────────────────


class TestWaitCommand:
    """Tests for the wait command."""

    @respx.mock
    def test_wait_until_done_json(self, runner, mock_task_done_response):
        respx.post("https://api.acedata.cloud/maestro/tasks").mock(
            return_value=Response(200, json=mock_task_done_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "wait", "maestro-task-123", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "succeeded"

    @respx.mock
    def test_wait_polls_until_done(self, runner, mock_task_response, mock_task_done_response):
        call_count = 0

        def side_effect(_request):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                return Response(200, json=mock_task_response)
            return Response(200, json=mock_task_done_response)

        respx.post("https://api.acedata.cloud/maestro/tasks").mock(side_effect=side_effect)
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "wait",
                "maestro-task-123",
                "--interval",
                "0",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "succeeded"

    @respx.mock
    def test_wait_failed_task(self, runner):
        failed_response = {
            "id": "maestro-task-123",
            "status": "failed",
        }
        respx.post("https://api.acedata.cloud/maestro/tasks").mock(
            return_value=Response(200, json=failed_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "wait", "maestro-task-123", "--json"],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_wait_api_error(self, runner, mock_error_response):
        respx.post("https://api.acedata.cloud/maestro/tasks").mock(
            return_value=Response(500, json=mock_error_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "wait", "maestro-task-123"],
        )
        assert result.exit_code != 0


# ─── Info Commands ────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info/utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0

    def test_config(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "config"])
        assert result.exit_code == 0

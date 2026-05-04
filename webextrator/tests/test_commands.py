"""Tests for WebExtrator CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from webextrator_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "webextrator-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "extract" in result.output
        assert "render" in result.output
        assert "tasks" in result.output
        assert "config" in result.output

    def test_help_extract(self, runner):
        result = runner.invoke(cli, ["extract", "--help"])
        assert result.exit_code == 0
        assert "URL" in result.output
        assert "--expected-type" in result.output

    def test_help_render(self, runner):
        result = runner.invoke(cli, ["render", "--help"])
        assert result.exit_code == 0
        assert "URL" in result.output
        assert "--wait-until" in result.output


# ─── Extract Commands ──────────────────────────────────────────────────────


class TestExtractCommands:
    """Tests for extract command."""

    @respx.mock
    def test_extract_json(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extract", "https://example.com", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "extract-task-123"

    @respx.mock
    def test_extract_rich_output(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extract", "https://example.com"],
        )
        assert result.exit_code == 0
        assert "extract-task-123" in result.output

    @respx.mock
    def test_extract_with_expected_type(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "extract",
                "https://example.com",
                "--expected-type",
                "product",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_extract_with_enable_llm(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extract", "https://example.com", "--enable-llm", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_extract_with_block_resources(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "extract",
                "https://example.com",
                "--block-resource",
                "image",
                "--block-resource",
                "font",
                "--json",
            ],
        )
        assert result.exit_code == 0

    def test_extract_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "extract", "https://example.com"])
        assert result.exit_code != 0


# ─── Render Commands ───────────────────────────────────────────────────────


class TestRenderCommands:
    """Tests for render command."""

    @respx.mock
    def test_render_json(self, runner, mock_render_response):
        respx.post("https://api.acedata.cloud/webextrator/render").mock(
            return_value=Response(200, json=mock_render_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "render", "https://example.com", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "render-task-123"

    @respx.mock
    def test_render_rich_output(self, runner, mock_render_response):
        respx.post("https://api.acedata.cloud/webextrator/render").mock(
            return_value=Response(200, json=mock_render_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "render", "https://example.com"],
        )
        assert result.exit_code == 0
        assert "render-task-123" in result.output

    @respx.mock
    def test_render_with_wait_until(self, runner, mock_render_response):
        respx.post("https://api.acedata.cloud/webextrator/render").mock(
            return_value=Response(200, json=mock_render_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "render",
                "https://example.com",
                "--wait-until",
                "load",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_render_with_callback_url(self, runner, mock_render_response):
        respx.post("https://api.acedata.cloud/webextrator/render").mock(
            return_value=Response(200, json=mock_render_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "render",
                "https://example.com",
                "--callback-url",
                "https://your.server.com/callback",
                "--json",
            ],
        )
        assert result.exit_code == 0

    def test_render_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "render", "https://example.com"])
        assert result.exit_code != 0


# ─── Tasks Commands ────────────────────────────────────────────────────────


class TestTasksCommands:
    """Tests for tasks commands."""

    @respx.mock
    def test_tasks_retrieve_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "retrieve", "--id", "extract-task-123", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "extract-task-123"

    @respx.mock
    def test_tasks_retrieve_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "retrieve", "--id", "extract-task-123"],
        )
        assert result.exit_code == 0

    def test_tasks_retrieve_requires_id_or_trace_id(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "retrieve"],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_tasks_retrieve_by_trace_id(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "retrieve",
                "--trace-id",
                "extract-trace-456",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_batch_response):
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=mock_task_batch_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "batch", "--ids", "task-1", "--ids", "task-2", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["count"] == 2

    @respx.mock
    def test_tasks_batch_rich_output(self, runner, mock_task_batch_response):
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=mock_task_batch_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tasks",
                "batch",
                "--trace-ids",
                "trace-1",
                "--trace-ids",
                "trace-2",
            ],
        )
        assert result.exit_code == 0


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

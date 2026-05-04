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

    def test_help_extract(self, runner):
        result = runner.invoke(cli, ["extract", "--help"])
        assert result.exit_code == 0
        assert "URL" in result.output

    def test_help_render(self, runner):
        result = runner.invoke(cli, ["render", "--help"])
        assert result.exit_code == 0
        assert "URL" in result.output


class TestExtractCommand:
    """Tests for the extract command."""

    @respx.mock
    def test_extract_json(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "extract", "https://www.amazon.com/dp/B0C1234567",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "550e8400-e29b-41d4-a716-446655440000"

    @respx.mock
    def test_extract_rich_output(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extract", "https://www.amazon.com/dp/B0C1234567"],
        )
        assert result.exit_code == 0
        assert "550e8400-e29b-41d4-a716-446655440000" in result.output

    @respx.mock
    def test_extract_with_expected_type(self, runner, mock_extract_response):
        respx.post("https://api.acedata.cloud/webextrator/extract").mock(
            return_value=Response(200, json=mock_extract_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "extract", "https://example.com",
                "--expected-type", "product", "--json",
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
            [
                "--token", "test-token",
                "extract", "https://example.com",
                "--enable-llm", "--json",
            ],
        )
        assert result.exit_code == 0

    def test_extract_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "extract", "https://example.com"])
        assert result.exit_code != 0


class TestRenderCommand:
    """Tests for the render command."""

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
        assert data["task_id"] == "550e8400-e29b-41d4-a716-446655440002"

    @respx.mock
    def test_render_rich_output(self, runner, mock_render_response):
        respx.post("https://api.acedata.cloud/webextrator/render").mock(
            return_value=Response(200, json=mock_render_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "render", "https://example.com"]
        )
        assert result.exit_code == 0
        assert "550e8400-e29b-41d4-a716-446655440002" in result.output

    @respx.mock
    def test_render_with_wait_until(self, runner, mock_render_response):
        respx.post("https://api.acedata.cloud/webextrator/render").mock(
            return_value=Response(200, json=mock_render_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "render", "https://example.com",
                "--wait-until", "load", "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_render_with_callback(self, runner, mock_render_response):
        respx.post("https://api.acedata.cloud/webextrator/render").mock(
            return_value=Response(200, json=mock_render_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "render", "https://example.com",
                "--callback-url", "https://my.server.com/webhook", "--json",
            ],
        )
        assert result.exit_code == 0

    def test_render_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "render", "https://example.com"])
        assert result.exit_code != 0


class TestTasksCommands:
    """Tests for tasks management commands."""

    @respx.mock
    def test_tasks_retrieve_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "tasks", "retrieve",
                "--id", "550e8400-e29b-41d4-a716-446655440000",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "550e8400-e29b-41d4-a716-446655440000"

    @respx.mock
    def test_tasks_retrieve_by_trace_id(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "tasks", "retrieve",
                "--trace-id", "550e8400-e29b-41d4-a716-446655440001",
                "--json",
            ],
        )
        assert result.exit_code == 0

    def test_tasks_retrieve_requires_id_or_trace_id(self, runner):
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "retrieve"]
        )
        assert result.exit_code != 0

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        batch_response = {"items": [mock_task_response], "count": 1}
        respx.post("https://api.acedata.cloud/webextrator/tasks").mock(
            return_value=Response(200, json=batch_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "tasks", "batch",
                "--ids", "id1", "--ids", "id2",
                "--json",
            ],
        )
        assert result.exit_code == 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

"""Tests for QRArt CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from qrart_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "qrart-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "--type" in result.output
        assert "--content" in result.output
        assert "--preset" in result.output


class TestGenerateCommand:
    """Tests for QR code generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_qr_response):
        route = respx.post("https://api.acedata.cloud/qrart/generate").mock(
            return_value=Response(200, json=mock_qr_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "A beautiful sunset",
                "--content", "https://example.com",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "abc123-def456"
        sent = json.loads(route.calls[0].request.content)
        assert sent["prompt"] == "A beautiful sunset"
        assert sent["content"] == "https://example.com"

    @respx.mock
    def test_generate_with_type(self, runner, mock_qr_response):
        route = respx.post("https://api.acedata.cloud/qrart/generate").mock(
            return_value=Response(200, json=mock_qr_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "A beautiful sunset",
                "--type", "text",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["type"] == "text"

    @respx.mock
    def test_generate_with_preset(self, runner, mock_qr_response):
        route = respx.post("https://api.acedata.cloud/qrart/generate").mock(
            return_value=Response(200, json=mock_qr_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "Futuristic city",
                "--preset", "neon-mech",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["preset"] == "neon-mech"

    @respx.mock
    def test_generate_with_pattern(self, runner, mock_qr_response):
        route = respx.post("https://api.acedata.cloud/qrart/generate").mock(
            return_value=Response(200, json=mock_qr_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "Cherry blossoms",
                "--pattern", "s1",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["pattern"] == "s1"

    @respx.mock
    def test_generate_async(self, runner, mock_qr_response):
        route = respx.post("https://api.acedata.cloud/qrart/generate").mock(
            return_value=Response(200, json=mock_qr_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "A beautiful sunset",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_generate_rich_output(self, runner, mock_qr_response):
        respx.post("https://api.acedata.cloud/qrart/generate").mock(
            return_value=Response(200, json=mock_qr_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token",
                "generate",
                "A beautiful sunset",
            ],
        )
        assert result.exit_code == 0
        assert "abc123-def456" in result.output

    def test_generate_no_token(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token", "",
                "generate",
                "A beautiful sunset",
            ],
        )
        assert result.exit_code != 0


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/qrart/tasks").mock(
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
        respx.post("https://api.acedata.cloud/qrart/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "abc123-def456"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/qrart/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "abc123", "def456", "--json"]
        )
        assert result.exit_code == 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_presets(self, runner):
        result = runner.invoke(cli, ["presets"])
        assert result.exit_code == 0
        assert "neon-mech" in result.output
        assert "sunset" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

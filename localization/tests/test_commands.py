"""Tests for Localization CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from localization_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "localization-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "translate" in result.output
        assert "config" in result.output

    def test_help_translate(self, runner):
        result = runner.invoke(cli, ["translate", "--help"])
        assert result.exit_code == 0
        assert "INPUT" in result.output
        assert "--locale" in result.output
        assert "--extension" in result.output


class TestTranslateCommand:
    """Tests for localization translation command."""

    @respx.mock
    def test_translate_markdown_json_output(self, runner, mock_translation_response):
        respx.post("https://api.acedata.cloud/localization/translate").mock(
            return_value=Response(200, json=mock_translation_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "translate",
                "# Title 1",
                "--locale",
                "zh-CN",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["locale"] == "zh-CN"

    @respx.mock
    def test_translate_markdown_payload(self, runner, mock_translation_response):
        route = respx.post("https://api.acedata.cloud/localization/translate").mock(
            return_value=Response(200, json=mock_translation_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "translate",
                "# Title 1",
                "--locale",
                "zh-CN",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["input"] == "# Title 1"
        assert sent["locale"] == "zh-CN"
        assert sent["extension"] == "md"
        assert "model" not in sent

    @respx.mock
    def test_translate_json_payload(self, runner, mock_translation_response):
        route = respx.post("https://api.acedata.cloud/localization/translate").mock(
            return_value=Response(200, json=mock_translation_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "translate",
                '{"message.clickButton":{"message":"Please click button to apply"}}',
                "--extension",
                "json",
                "--locale",
                "zh-CN",
                "--model",
                "gpt-4",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["input"] == {
            "message.clickButton": {"message": "Please click button to apply"}
        }
        assert sent["extension"] == "json"
        assert sent["model"] == "gpt-4"

    def test_translate_json_rejects_non_object_input(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "translate",
                '["not", "object"]',
                "--extension",
                "json",
                "--locale",
                "zh-CN",
            ],
        )
        assert result.exit_code != 0
        assert "JSON object" in result.output

    def test_translate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "translate", "# Title", "--locale", "zh-CN"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

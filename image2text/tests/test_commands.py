"""Tests for Image2Text CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from image2text_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "image2text-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "recognize" in result.output
        assert "config" in result.output

    def test_help_recognize(self, runner):
        result = runner.invoke(cli, ["recognize", "--help"])
        assert result.exit_code == 0
        assert "IMAGE" in result.output
        assert "--async" in result.output


class TestRecognizeCommand:
    """Tests for image2text recognition command."""

    @respx.mock
    def test_recognize_json(self, runner, mock_recognition_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/image2text").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "https://example.com/captcha.png",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["text"] == "AB12CD"

    @respx.mock
    def test_recognize_rich_output(self, runner, mock_recognition_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/image2text").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "https://example.com/captcha.png",
            ],
        )
        assert result.exit_code == 0
        assert "AB12CD" in result.output

    @respx.mock
    def test_recognize_sends_correct_payload(self, runner, mock_recognition_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/image2text").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "https://example.com/captcha.png",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["image"] == "https://example.com/captcha.png"
        assert "async" not in sent

    @respx.mock
    def test_recognize_async(self, runner, mock_recognition_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/image2text").mock(
            return_value=Response(200, json=mock_recognition_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "https://example.com/captcha.png",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_recognize_async_rich_output(self, runner, mock_recognition_async_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/image2text").mock(
            return_value=Response(200, json=mock_recognition_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "https://example.com/captcha.png",
                "--async",
            ],
        )
        assert result.exit_code == 0
        assert "3a8b1c2d" in result.output

    def test_recognize_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "recognize", "https://example.com/captcha.png"])
        assert result.exit_code != 0

    def test_recognize_missing_image(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "recognize"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

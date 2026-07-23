"""Tests for recaptcha CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from recaptcha_cli.main import cli

SAMPLE_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
SAMPLE_WEBSITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
SAMPLE_WEBSITE_URL = "https://example.com"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "recaptcha-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "recognize" in result.output
        assert "token" in result.output
        assert "token3" in result.output
        assert "config" in result.output

    def test_help_recognize(self, runner):
        result = runner.invoke(cli, ["recognize", "--help"])
        assert result.exit_code == 0
        assert "IMAGE" in result.output
        assert "QUESTION" in result.output
        assert "--async" in result.output

    def test_help_token(self, runner):
        result = runner.invoke(cli, ["token", "--help"])
        assert result.exit_code == 0
        assert "WEBSITE_KEY" in result.output
        assert "WEBSITE_URL" in result.output
        assert "--async" in result.output

    def test_help_token3(self, runner):
        result = runner.invoke(cli, ["token3", "--help"])
        assert result.exit_code == 0
        assert "WEBSITE_KEY" in result.output
        assert "WEBSITE_URL" in result.output
        assert "PAGE_ACTION" in result.output
        assert "--async" in result.output


class TestRecognizeCommand:
    """Tests for reCAPTCHA v2 recognition command."""

    @respx.mock
    def test_recognize_json(self, runner, mock_recognition_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                SAMPLE_IMAGE,
                "/m/0k4j",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "solution" in data

    @respx.mock
    def test_recognize_rich_output(self, runner, mock_recognition_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                SAMPLE_IMAGE,
                "/m/0k4j",
            ],
        )
        assert result.exit_code == 0
        assert "Recognition Result" in result.output

    @respx.mock
    def test_recognize_sends_correct_payload(self, runner, mock_recognition_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                SAMPLE_IMAGE,
                "/m/0k4j",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["image"] == SAMPLE_IMAGE
        assert sent["question"] == "/m/0k4j"
        assert "async" not in sent

    @respx.mock
    def test_recognize_async(self, runner, mock_recognition_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                SAMPLE_IMAGE,
                "/m/0k4j",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_recognize_async_rich_output(self, runner, mock_recognition_async_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                SAMPLE_IMAGE,
                "/m/0k4j",
                "--async",
            ],
        )
        assert result.exit_code == 0
        assert "Recognition Task Submitted" in result.output
        assert "3a8b1c2d" in result.output

    def test_recognize_no_token(self, runner):
        result = runner.invoke(
            cli, ["--token", "", "recognize", SAMPLE_IMAGE, "/m/0k4j"]
        )
        assert result.exit_code != 0

    def test_recognize_missing_args(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "recognize"])
        assert result.exit_code != 0


class TestTokenCommand:
    """Tests for reCAPTCHA v2 token command."""

    @respx.mock
    def test_token_json(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "token" in data

    @respx.mock
    def test_token_rich_output(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
            ],
        )
        assert result.exit_code == 0
        assert "03AGdBq25SxXT" in result.output

    @respx.mock
    def test_token_sends_correct_payload(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["website_key"] == SAMPLE_WEBSITE_KEY
        assert sent["website_url"] == SAMPLE_WEBSITE_URL
        assert "async" not in sent

    @respx.mock
    def test_token_async(self, runner, mock_token_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_token_async_rich_output(self, runner, mock_token_async_response):
        respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "--async",
            ],
        )
        assert result.exit_code == 0
        assert "3a8b1c2d" in result.output

    def test_token_no_token(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "",
                "token",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
            ],
        )
        assert result.exit_code != 0

    def test_token_missing_args(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "token"])
        assert result.exit_code != 0


class TestToken3Command:
    """Tests for reCAPTCHA v3 token command."""

    @respx.mock
    def test_token3_json(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/recaptcha3").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token3",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "login",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "token" in data

    @respx.mock
    def test_token3_rich_output(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/recaptcha3").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token3",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "login",
            ],
        )
        assert result.exit_code == 0
        assert "03AGdBq25SxXT" in result.output

    @respx.mock
    def test_token3_sends_correct_payload(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha3").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token3",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "login",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["website_key"] == SAMPLE_WEBSITE_KEY
        assert sent["website_url"] == SAMPLE_WEBSITE_URL
        assert sent["page_action"] == "login"
        assert "async" not in sent

    @respx.mock
    def test_token3_async(self, runner, mock_token_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha3").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token3",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "login",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_token3_async_rich_output(self, runner, mock_token_async_response):
        respx.post("https://api.acedata.cloud/captcha/token/recaptcha3").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token3",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "login",
                "--async",
            ],
        )
        assert result.exit_code == 0
        assert "3a8b1c2d" in result.output

    def test_token3_no_token(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "",
                "token3",
                SAMPLE_WEBSITE_KEY,
                SAMPLE_WEBSITE_URL,
                "login",
            ],
        )
        assert result.exit_code != 0

    def test_token3_missing_args(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "token3"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

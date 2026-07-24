"""Tests for reCAPTCHA CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from recaptcha_cli.main import cli


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
        assert "recognize2" in result.output
        assert "token2" in result.output
        assert "token3" in result.output
        assert "config" in result.output

    def test_help_recognize2(self, runner):
        result = runner.invoke(cli, ["recognize2", "--help"])
        assert result.exit_code == 0
        assert "IMAGE" in result.output
        assert "QUESTION" in result.output
        assert "--async" in result.output

    def test_help_token2(self, runner):
        result = runner.invoke(cli, ["token2", "--help"])
        assert result.exit_code == 0
        assert "WEBSITE_KEY" in result.output
        assert "WEBSITE_URL" in result.output
        assert "--proxy" in result.output
        assert "--async" in result.output

    def test_help_token3(self, runner):
        result = runner.invoke(cli, ["token3", "--help"])
        assert result.exit_code == 0
        assert "WEBSITE_KEY" in result.output
        assert "WEBSITE_URL" in result.output
        assert "--page-action" in result.output
        assert "--async" in result.output


class TestRecognize2Command:
    """Tests for reCAPTCHA v2 recognition command."""

    @respx.mock
    def test_recognize2_json(self, runner, mock_recognition_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize2",
                "https://example.com/captcha.jpg",
                "Select all cars",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "solution" in data

    @respx.mock
    def test_recognize2_sends_correct_payload(self, runner, mock_recognition_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize2",
                "https://example.com/captcha.jpg",
                "Select all vehicles",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["image"] == "https://example.com/captcha.jpg"
        assert sent["question"] == "Select all vehicles"
        assert "async" not in sent

    @respx.mock
    def test_recognize2_async(self, runner, mock_recognition_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
            return_value=Response(200, json=mock_recognition_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize2",
                "https://example.com/captcha.jpg",
                "Select all cars",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_recognize2_missing_args(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "recognize2"])
        assert result.exit_code != 0

    def test_recognize2_no_token(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "", "recognize2", "https://example.com/captcha.jpg", "Select all cars"],
        )
        assert result.exit_code != 0


class TestToken2Command:
    """Tests for reCAPTCHA v2 token command."""

    @respx.mock
    def test_token2_json(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token2",
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "token" in data

    @respx.mock
    def test_token2_sends_correct_payload(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token2",
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["website_key"] == "6LcXxxxxxxxxxxxxxx"
        assert sent["website_url"] == "https://example.com"
        assert "proxy" not in sent
        assert "async" not in sent

    @respx.mock
    def test_token2_with_proxy(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token2",
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
                "--proxy",
                "http://127.0.0.1:8080",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["proxy"] == "http://127.0.0.1:8080"

    @respx.mock
    def test_token2_async(self, runner, mock_token_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token2",
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_token2_missing_args(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "token2"])
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
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
                "--page-action",
                "submit",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "token" in data

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
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
                "--page-action",
                "login",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["website_key"] == "6LcXxxxxxxxxxxxxxx"
        assert sent["website_url"] == "https://example.com"
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
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
                "--page-action",
                "submit",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_token3_missing_page_action(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token3",
                "6LcXxxxxxxxxxxxxxx",
                "https://example.com",
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

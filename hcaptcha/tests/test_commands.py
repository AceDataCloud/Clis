"""Tests for hCaptcha CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from hcaptcha_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "hcaptcha-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "recognize" in result.output
        assert "token" in result.output
        assert "config" in result.output

    def test_help_recognize(self, runner):
        result = runner.invoke(cli, ["recognize", "--help"])
        assert result.exit_code == 0
        assert "--queries" in result.output
        assert "--question" in result.output
        assert "--async" in result.output

    def test_help_token(self, runner):
        result = runner.invoke(cli, ["token", "--help"])
        assert result.exit_code == 0
        assert "WEBSITE_KEY" in result.output
        assert "WEBSITE_URL" in result.output
        assert "--async" in result.output


class TestRecognizeCommand:
    """Tests for hCaptcha recognition command."""

    @respx.mock
    def test_recognize_json(self, runner, mock_recognition_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "--queries",
                '["https://example.com/img1.jpg"]',
                "--question",
                "Select all cars",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "solution" in data

    @respx.mock
    def test_recognize_rich_output(self, runner, mock_recognition_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "--queries",
                '["https://example.com/img1.jpg"]',
            ],
        )
        assert result.exit_code == 0
        assert "Recognition Result" in result.output

    @respx.mock
    def test_recognize_sends_correct_payload(self, runner, mock_recognition_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
            return_value=Response(200, json=mock_recognition_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "--queries",
                '["https://example.com/img1.jpg", "https://example.com/img2.jpg"]',
                "--question",
                "Select all vehicles",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["queries"] == [
            "https://example.com/img1.jpg",
            "https://example.com/img2.jpg",
        ]
        assert sent["question"] == "Select all vehicles"
        assert "async" not in sent

    @respx.mock
    def test_recognize_async(self, runner, mock_recognition_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
            return_value=Response(200, json=mock_recognition_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "--queries",
                '["https://example.com/img1.jpg"]',
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_recognize_async_rich_output(self, runner, mock_recognition_async_response):
        respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
            return_value=Response(200, json=mock_recognition_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "recognize",
                "--queries",
                '["https://example.com/img1.jpg"]',
                "--async",
            ],
        )
        assert result.exit_code == 0
        assert "Recognition Task Submitted" in result.output
        assert "3a8b1c2d" in result.output

    def test_recognize_invalid_queries_json(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "recognize", "--queries", "not-json"],
        )
        assert result.exit_code != 0
        assert "--queries must be valid JSON." in result.output

    def test_recognize_queries_not_array(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "recognize", "--queries", '{"key": "value"}'],
        )
        assert result.exit_code != 0
        assert "--queries must be a JSON array." in result.output

    def test_recognize_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "recognize"])
        assert result.exit_code != 0


class TestTokenCommand:
    """Tests for hCaptcha token command."""

    @respx.mock
    def test_token_json(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
                "https://accounts.hcaptcha.com/demo",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "token" in data

    @respx.mock
    def test_token_rich_output(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
                "https://accounts.hcaptcha.com/demo",
            ],
        )
        assert result.exit_code == 0
        assert "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test-token" in result.output

    @respx.mock
    def test_token_sends_correct_payload(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
                "https://accounts.hcaptcha.com/demo",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["website_key"] == "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2"
        assert sent["website_url"] == "https://accounts.hcaptcha.com/demo"
        assert "async" not in sent

    @respx.mock
    def test_token_async(self, runner, mock_token_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
                "https://accounts.hcaptcha.com/demo",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_token_async_rich_output(self, runner, mock_token_async_response):
        respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
                "https://accounts.hcaptcha.com/demo",
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
                "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
                "https://accounts.hcaptcha.com/demo",
            ],
        )
        assert result.exit_code != 0

    def test_token_missing_args(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "token"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

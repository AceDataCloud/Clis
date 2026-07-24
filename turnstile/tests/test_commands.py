"""Tests for Turnstile CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from turnstile_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "turnstile-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "token" in result.output
        assert "config" in result.output

    def test_help_token(self, runner):
        result = runner.invoke(cli, ["token", "--help"])
        assert result.exit_code == 0
        assert "WEBSITE_KEY" in result.output
        assert "WEBSITE_URL" in result.output
        assert "--action" in result.output
        assert "--cdata" in result.output
        assert "--async" in result.output


class TestTokenCommand:
    """Tests for Turnstile token command."""

    @respx.mock
    def test_token_json(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "token" in data

    @respx.mock
    def test_token_rich_output(self, runner, mock_token_response):
        respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
            ],
        )
        assert result.exit_code == 0
        assert "0.zScW-EiocHwwpwqtk1QXlJnGnU.test-token" in result.output

    @respx.mock
    def test_token_sends_correct_payload(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["website_key"] == "0x4AAAAAAADnPIDROrmt1Wwj"
        assert sent["website_url"] == "https://react-turnstile.vercel.app"
        assert "async" not in sent
        assert "action" not in sent
        assert "cdata" not in sent

    @respx.mock
    def test_token_with_action(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
                "--action",
                "login",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["action"] == "login"

    @respx.mock
    def test_token_with_cdata(self, runner, mock_token_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
            return_value=Response(200, json=mock_token_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
                "--cdata",
                "some-cdata",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["cdata"] == "some-cdata"

    @respx.mock
    def test_token_async(self, runner, mock_token_async_response):
        route = respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_token_async_rich_output(self, runner, mock_token_async_response):
        respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
            return_value=Response(200, json=mock_token_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "token",
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
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
                "0x4AAAAAAADnPIDROrmt1Wwj",
                "https://react-turnstile.vercel.app",
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

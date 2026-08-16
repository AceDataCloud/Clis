"""Tests for Discord Bot CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from discord_bot_cli.main import cli

BASE_URL = "https://discord-bot-test.app.acedata.cloud"
TOKEN = "test-token"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def invoke(runner: CliRunner, args: list[str]) -> object:
    """Helper to invoke CLI with base-url and token."""
    return runner.invoke(
        cli,
        ["--base-url", BASE_URL, "--token", TOKEN, *args],
    )


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "discord-bot-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "health" in result.output
        assert "whoami" in result.output
        assert "guilds" in result.output

    def test_help_send(self, runner):
        result = runner.invoke(cli, ["send", "--help"])
        assert result.exit_code == 0
        assert "CHANNEL_ID" in result.output

    def test_help_messages(self, runner):
        result = runner.invoke(cli, ["messages", "--help"])
        assert result.exit_code == 0
        assert "CHANNEL_ID" in result.output


class TestHealthCommand:
    """Tests for the health command."""

    @respx.mock
    def test_health_ok(self, runner, mock_health_response):
        respx.get(f"{BASE_URL}/health").mock(
            return_value=Response(200, json=mock_health_response)
        )
        result = invoke(runner, ["health"])
        assert result.exit_code == 0
        assert "ok" in result.output

    @respx.mock
    def test_health_json(self, runner, mock_health_response):
        respx.get(f"{BASE_URL}/health").mock(
            return_value=Response(200, json=mock_health_response)
        )
        result = invoke(runner, ["health", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "ok"
        assert data["gateway_ready"] is True

    @respx.mock
    def test_health_gateway_not_ready(self, runner):
        respx.get(f"{BASE_URL}/health").mock(
            return_value=Response(200, json={"status": "ok", "gateway_ready": False})
        )
        result = invoke(runner, ["health", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["gateway_ready"] is False


class TestWhoamiCommand:
    """Tests for the whoami command."""

    @respx.mock
    def test_whoami_json(self, runner, mock_whoami_response):
        respx.get(f"{BASE_URL}/api/whoami").mock(
            return_value=Response(200, json=mock_whoami_response)
        )
        result = invoke(runner, ["whoami", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["username"] == "testuser"

    @respx.mock
    def test_whoami_rich(self, runner, mock_whoami_response):
        respx.get(f"{BASE_URL}/api/whoami").mock(
            return_value=Response(200, json=mock_whoami_response)
        )
        result = invoke(runner, ["whoami"])
        assert result.exit_code == 0
        assert "testuser" in result.output

    def test_whoami_no_base_url(self, runner):
        result = runner.invoke(cli, ["--token", TOKEN, "whoami"])
        assert result.exit_code != 0


class TestGuildsCommands:
    """Tests for guild-related commands."""

    @respx.mock
    def test_guilds_json(self, runner, mock_guilds_response):
        respx.get(f"{BASE_URL}/api/guilds").mock(
            return_value=Response(200, json=mock_guilds_response)
        )
        result = invoke(runner, ["guilds", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["data"]) == 2

    @respx.mock
    def test_guilds_rich(self, runner, mock_guilds_response):
        respx.get(f"{BASE_URL}/api/guilds").mock(
            return_value=Response(200, json=mock_guilds_response)
        )
        result = invoke(runner, ["guilds"])
        assert result.exit_code == 0
        assert "My Server" in result.output

    @respx.mock
    def test_channels_json(self, runner, mock_channels_response):
        respx.get(f"{BASE_URL}/api/guilds/1234567890/channels").mock(
            return_value=Response(200, json=mock_channels_response)
        )
        result = invoke(runner, ["channels", "1234567890", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["data"]) == 2

    @respx.mock
    def test_create_channel_json(self, runner):
        respx.post(f"{BASE_URL}/api/guilds/1234567890/channels").mock(
            return_value=Response(200, json={"data": {"id": "333000333", "name": "new-channel"}})
        )
        result = invoke(runner, ["create-channel", "1234567890", "new-channel", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["name"] == "new-channel"

    @respx.mock
    def test_members_json(self, runner, mock_members_response):
        respx.get(f"{BASE_URL}/api/guilds/1234567890/members").mock(
            return_value=Response(200, json=mock_members_response)
        )
        result = invoke(runner, ["members", "1234567890", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["data"]) == 2

    @respx.mock
    def test_members_with_limit(self, runner, mock_members_response):
        route = respx.get(f"{BASE_URL}/api/guilds/1234567890/members").mock(
            return_value=Response(200, json=mock_members_response)
        )
        result = invoke(runner, ["members", "1234567890", "--limit", "10", "--json"])
        assert result.exit_code == 0
        assert "limit=10" in str(route.calls[0].request.url)


class TestMessageCommands:
    """Tests for message-related commands."""

    @respx.mock
    def test_send_json(self, runner, mock_message_response):
        route = respx.post(f"{BASE_URL}/api/messages").mock(
            return_value=Response(200, json=mock_message_response)
        )
        result = invoke(runner, ["send", "1234567890", "Hello!", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["content"] == "Hello!"
        sent = json.loads(route.calls[0].request.content)
        assert sent["channel_id"] == "1234567890"
        assert sent["content"] == "Hello!"

    @respx.mock
    def test_send_with_reply_to(self, runner, mock_message_response):
        route = respx.post(f"{BASE_URL}/api/messages").mock(
            return_value=Response(200, json=mock_message_response)
        )
        result = invoke(runner, ["send", "1234567890", "Got it", "--reply-to", "9876543210", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["reply_to"] == "9876543210"

    @respx.mock
    def test_send_with_idempotency_key(self, runner, mock_message_response):
        route = respx.post(f"{BASE_URL}/api/messages").mock(
            return_value=Response(200, json=mock_message_response)
        )
        result = invoke(
            runner,
            [
                "send",
                "1234567890",
                "Hello!",
                "--idempotency-key",
                "msg-20260816-001",
                "--json",
            ],
        )
        assert result.exit_code == 0
        assert route.calls[0].request.headers["idempotency-key"] == "msg-20260816-001"

    @respx.mock
    def test_messages_json(self, runner, mock_messages_response):
        respx.get(f"{BASE_URL}/api/channels/1234567890/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = invoke(runner, ["messages", "1234567890", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["data"]) == 2

    @respx.mock
    def test_messages_with_limit(self, runner, mock_messages_response):
        route = respx.get(f"{BASE_URL}/api/channels/1234567890/messages").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = invoke(runner, ["messages", "1234567890", "--limit", "20", "--json"])
        assert result.exit_code == 0
        assert "limit=20" in str(route.calls[0].request.url)

    @respx.mock
    def test_search_json(self, runner, mock_messages_response):
        route = respx.get(f"{BASE_URL}/api/channels/1234567890/messages/search").mock(
            return_value=Response(200, json=mock_messages_response)
        )
        result = invoke(runner, ["search", "1234567890", "release date", "--json"])
        assert result.exit_code == 0
        assert "q=release+date" in str(route.calls[0].request.url) or "q=release" in str(
            route.calls[0].request.url
        )

    @respx.mock
    def test_edit_json(self, runner, mock_message_response):
        route = respx.patch(f"{BASE_URL}/api/channels/1234567890/messages/9876543210").mock(
            return_value=Response(200, json=mock_message_response)
        )
        result = invoke(runner, ["edit", "1234567890", "9876543210", "Updated text", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["content"] == "Updated text"

    @respx.mock
    def test_delete(self, runner):
        respx.delete(f"{BASE_URL}/api/channels/1234567890/messages/9876543210").mock(
            return_value=Response(200, json={"data": {}})
        )
        result = invoke(runner, ["delete", "1234567890", "9876543210"])
        assert result.exit_code == 0

    @respx.mock
    def test_react_json(self, runner):
        route = respx.post(
            f"{BASE_URL}/api/channels/1234567890/messages/9876543210/reactions"
        ).mock(return_value=Response(200, json={"data": {}}))
        result = invoke(runner, ["react", "1234567890", "9876543210", "👍", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["emoji"] == "👍"

    @respx.mock
    def test_pin(self, runner):
        respx.post(
            f"{BASE_URL}/api/channels/1234567890/messages/9876543210/pin"
        ).mock(return_value=Response(200, json={"data": {}}))
        result = invoke(runner, ["pin", "1234567890", "9876543210"])
        assert result.exit_code == 0


class TestDMCommands:
    """Tests for DM commands."""

    @respx.mock
    def test_open_dm_json(self, runner, mock_channel_response):
        route = respx.post(f"{BASE_URL}/api/dms").mock(
            return_value=Response(200, json=mock_channel_response)
        )
        result = invoke(runner, ["open-dm", "111222333444555666", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == "777888999"
        sent = json.loads(route.calls[0].request.content)
        assert sent["recipient_id"] == "111222333444555666"

    @respx.mock
    def test_send_dm_json(self, runner, mock_message_response):
        route = respx.post(f"{BASE_URL}/api/dms/send").mock(
            return_value=Response(200, json=mock_message_response)
        )
        result = invoke(runner, ["send-dm", "111222333444555666", "Hello!", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["recipient_id"] == "111222333444555666"
        assert sent["content"] == "Hello!"


class TestErrorHandling:
    """Tests for error handling."""

    @respx.mock
    def test_unauthorized(self, runner):
        respx.get(f"{BASE_URL}/api/whoami").mock(
            return_value=Response(401, json={"error": "unauthorized"})
        )
        result = invoke(runner, ["whoami"])
        assert result.exit_code != 0
        assert "Error" in result.output or "error" in result.output.lower()

    @respx.mock
    def test_service_unavailable(self, runner):
        respx.get(f"{BASE_URL}/api/whoami").mock(
            return_value=Response(503, json={"error": "gateway not ready"})
        )
        result = invoke(runner, ["whoami"])
        assert result.exit_code != 0

    def test_missing_base_url(self, runner):
        result = runner.invoke(cli, ["--token", TOKEN, "whoami"])
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "Discord Bot CLI" in result.output

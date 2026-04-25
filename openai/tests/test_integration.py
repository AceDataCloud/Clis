"""Integration tests for the OpenAI CLI (require real API access)."""

import pytest
from click.testing import CliRunner

from openai_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.mark.integration
class TestChatIntegration:
    """Integration tests for chat commands."""

    def test_chat_real_api(self, runner, api_token):
        result = runner.invoke(
            cli,
            ["--token", api_token, "chat", "Say 'hello' and nothing else.", "-m", "gpt-4o-mini"],
        )
        assert result.exit_code == 0


@pytest.mark.integration
class TestEmbedIntegration:
    """Integration tests for embed commands."""

    def test_embed_real_api(self, runner, api_token):
        result = runner.invoke(
            cli,
            ["--token", api_token, "embed", "Hello world", "-m", "text-embedding-3-small"],
        )
        assert result.exit_code == 0

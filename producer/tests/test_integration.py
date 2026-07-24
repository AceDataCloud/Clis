"""Integration tests for Producer CLI (requires API token)."""

import pytest
from click.testing import CliRunner

from producer_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGenerateIntegration:
    """Integration tests that require a real API token."""

    @pytest.mark.integration
    def test_generate_real_api(self, runner, api_token):
        result = runner.invoke(
            cli,
            ["--token", api_token, "generate", "A simple test music track", "--json"],
        )
        assert result.exit_code == 0


class TestInfoIntegration:
    """Integration tests for info commands (no token needed)."""

    def test_models_no_token(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "FUZZ" in result.output

    def test_actions_no_token(self, runner):
        result = runner.invoke(cli, ["actions"])
        assert result.exit_code == 0
        assert "generate" in result.output

"""Integration tests for Sora CLI (requires API token)."""

import pytest
from click.testing import CliRunner

from sora_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGenerateIntegration:
    """Integration tests that require a real API token."""

    @pytest.mark.integration
    def test_generate_real_api(self, runner, api_token):
        result = runner.invoke(
            cli,
            ["--token", api_token, "generate", "A simple test video", "--json"],
        )
        assert result.exit_code == 0


class TestInfoIntegration:
    """Integration tests for info commands (no token needed)."""

    def test_models_no_token(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "sora-2" in result.output

    def test_config_display(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

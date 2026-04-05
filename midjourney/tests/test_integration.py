"""Integration tests for Midjourney CLI (requires API token)."""

import pytest
from click.testing import CliRunner

from midjourney_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestImagineIntegration:
    """Integration tests that require a real API token."""

    @pytest.mark.integration
    def test_imagine_real_api(self, runner, api_token):
        result = runner.invoke(
            cli,
            ["--token", api_token, "imagine", "A simple test image", "--json"],
        )
        assert result.exit_code == 0


class TestInfoIntegration:
    """Integration tests for info commands (no token needed)."""

    def test_modes_no_token(self, runner):
        result = runner.invoke(cli, ["modes"])
        assert result.exit_code == 0
        assert "fast" in result.output

    def test_versions_no_token(self, runner):
        result = runner.invoke(cli, ["versions"])
        assert result.exit_code == 0
        assert "8" in result.output

    def test_config_display(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

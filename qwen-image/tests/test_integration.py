"""Integration tests for QwenImage CLI (requires API token)."""

import pytest
from click.testing import CliRunner

from qwen_image_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGenerateIntegration:
    """Integration tests that require a real API token."""

    @pytest.mark.integration
    def test_generate_real_api(self, runner, api_token):
        result = runner.invoke(
            cli,
            ["--token", api_token, "generate", "A simple red circle on white background", "--json"],
        )
        assert result.exit_code == 0

    @pytest.mark.integration
    def test_edit_real_api(self, runner, api_token):
        result = runner.invoke(
            cli,
            [
                "--token",
                api_token,
                "edit",
                "Make it look like a painting",
                "-i",
                "https://cdn.example.com/sample.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0


class TestInfoIntegration:
    """Integration tests for info commands (no token needed)."""

    def test_models_no_token(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "qwen-image-3.0" in result.output

    def test_prompt_extend_modes_no_token(self, runner):
        result = runner.invoke(cli, ["prompt-extend-modes"])
        assert result.exit_code == 0
        assert "direct" in result.output

    def test_config_display(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

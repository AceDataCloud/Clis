"""Integration tests for HappyHorse CLI (require real API token)."""

import pytest
from click.testing import CliRunner

from happyhorse_cli.main import cli


@pytest.mark.integration
class TestIntegration:
    """Integration tests that require a real API token."""

    def test_generate_video(self, api_token):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["--token", api_token, "generate", "A horse galloping through a field", "--json"],
        )
        assert result.exit_code == 0

    def test_image_to_video(self, api_token):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--token",
                api_token,
                "image-to-video",
                "Animate this scene",
                "--image-url",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/640px-Cat03.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0

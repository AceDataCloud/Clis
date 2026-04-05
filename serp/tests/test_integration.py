"""Integration tests for SERP CLI.

These tests require a valid ACEDATACLOUD_API_TOKEN environment variable.
They make real API calls and are skipped by default.
"""

import pytest


@pytest.mark.integration
@pytest.mark.slow
class TestSerpIntegration:
    """Integration tests requiring a real API token."""

    def test_web_search(self, api_token):
        from serp_cli.core.client import SerpClient

        client = SerpClient(api_token=api_token)
        result = client.search(query="hello world", type="search", number=3)
        assert "organic" in result or "answer_box" in result

    def test_news_search(self, api_token):
        from serp_cli.core.client import SerpClient

        client = SerpClient(api_token=api_token)
        result = client.search(query="technology", type="news", number=3)
        assert "news" in result

    def test_cli_search_integration(self, api_token):
        from click.testing import CliRunner

        from serp_cli.main import cli

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--token",
                api_token,
                "search",
                "hello world",
                "-n",
                "3",
                "--json",
            ],
        )
        assert result.exit_code == 0

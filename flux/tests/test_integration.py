"""Integration tests for Flux CLI.

These tests require a valid ACEDATACLOUD_API_TOKEN environment variable.
They make real API calls and are skipped by default.
"""

import pytest


@pytest.mark.integration
@pytest.mark.slow
class TestFluxIntegration:
    """Integration tests requiring a real API token."""

    def test_generate_image(self, api_token):
        from flux_cli.core.client import FluxClient

        client = FluxClient(api_token=api_token)
        result = client.generate_image(
            action="generate",
            prompt="A simple red circle on a white background, minimalist",
            model="flux-dev",
        )
        assert "task_id" in result or "data" in result

    def test_query_nonexistent_task(self, api_token):
        from flux_cli.core.client import FluxClient
        from flux_cli.core.exceptions import FluxAPIError

        client = FluxClient(api_token=api_token)
        with pytest.raises(FluxAPIError):
            client.query_task(id="nonexistent-task-id", action="retrieve")

    def test_generate_with_model(self, api_token):
        from flux_cli.core.client import FluxClient

        client = FluxClient(api_token=api_token)
        result = client.generate_image(
            action="generate",
            prompt="A blue square, flat design",
            model="flux-dev",
            size="512x512",
        )
        assert "task_id" in result or "data" in result

    def test_cli_generate_integration(self, api_token):
        from click.testing import CliRunner

        from flux_cli.main import cli

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--token",
                api_token,
                "generate",
                "A tiny green dot, minimalist",
                "--json",
            ],
        )
        assert result.exit_code == 0

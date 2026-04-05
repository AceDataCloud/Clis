"""Integration tests requiring real API access."""

import pytest

from adc_cli.core.client import AdcClient


@pytest.mark.integration
class TestIntegration:
    """Integration tests against the real AceDataCloud API."""

    def test_serp_search(self, api_token):
        client = AdcClient(api_token=api_token)
        result = client.serp_search(query="python programming", type="search", number=3)
        assert "organic" in result or "error" not in result

    def test_flux_image(self, api_token):
        client = AdcClient(api_token=api_token)
        result = client.flux_image(
            action="generate",
            prompt="A simple test image of a blue circle",
            model="flux-dev",
        )
        assert "task_id" in result or "data" in result

    def test_query_task_invalid(self, api_token):
        import contextlib

        client = AdcClient(api_token=api_token)
        with contextlib.suppress(Exception):
            client.query_task("flux", id="nonexistent-id", action="retrieve")

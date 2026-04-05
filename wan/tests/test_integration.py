"""Integration tests that require real API access."""

import pytest

from wan_cli.core.client import WanClient


@pytest.mark.integration
def test_generate_video_integration(api_token):
    """Test real video generation (requires API token)."""
    client = WanClient(api_token=api_token)
    result = client.generate_video(
        action="text2video",
        prompt="A simple test video of a sunrise",
        model="wan2.6-t2v",
    )
    assert result is not None
    assert "task_id" in result or "data" in result

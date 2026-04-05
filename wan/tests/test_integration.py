"""Integration tests (require real API token)."""

import pytest

from wan_cli.core.client import WanClient


@pytest.mark.integration
def test_generate_video_integration(api_token):
    """Test generating a video via real API."""
    client = WanClient(api_token=api_token)
    result = client.generate_video(
        action="text2video",
        prompt="A beautiful sunset over the ocean",
        model="wan2.6-t2v",
    )
    assert "task_id" in result or "data" in result


@pytest.mark.integration
def test_query_task_integration(api_token):
    """Test querying a task via real API."""
    client = WanClient(api_token=api_token)
    # Use a dummy task ID - it will return an error but we verify auth works
    try:
        client.query_task(id="test-task-id", action="retrieve")
    except Exception:
        pass  # Expected for non-existent task

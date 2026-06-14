"""Tests for HTTP client."""

import json

import respx
from httpx import Response

from kling_cli.core.client import KlingClient


class TestKlingClient:
    """Tests for KlingClient async callback behavior."""

    @respx.mock
    def test_generate_video_sets_async_without_callback(self):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json={"success": True, "task_id": "gen-123"})
        )
        client = KlingClient(api_token="test-token")
        client.generate_video(prompt="test", action="text2video")
        body = json.loads(route.calls.last.request.content)
        assert body["async"] is True

    @respx.mock
    def test_generate_motion_keeps_callback_without_forcing_async(self):
        route = respx.post("https://api.acedata.cloud/kling/motion").mock(
            return_value=Response(200, json={"success": True, "task_id": "mot-123"})
        )
        client = KlingClient(api_token="test-token")
        client.generate_motion(
            image_url="https://example.com/a.png",
            video_url="https://example.com/b.mp4",
            callback_url="https://example.com/callback",
        )
        body = json.loads(route.calls.last.request.content)
        assert body["callback_url"] == "https://example.com/callback"
        assert "async" not in body

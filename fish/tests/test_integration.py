"""Integration tests (require real API access)."""

import pytest

from fish_cli.core.client import FishClient


@pytest.mark.integration
class TestIntegration:
    """Integration tests that call the real Fish API."""

    def test_tts_basic(self, api_token):
        """Test basic TTS synthesis."""
        client = FishClient(api_token=api_token)
        result = client.synthesize(text="Hello, this is a test.")
        assert "audio_url" in result or "task_id" in result

    def test_list_voices(self, api_token):
        """Test listing voice models."""
        client = FishClient(api_token=api_token)
        result = client.list_voices(page_size=5)
        assert "total" in result
        assert "items" in result

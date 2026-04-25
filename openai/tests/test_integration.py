"""Placeholder for integration tests (require real API token)."""

import pytest


@pytest.mark.integration
class TestChatIntegration:
    """Integration tests for chat completions (requires API token)."""

    def test_basic_chat(self, api_token):
        from openai_cli.core.client import OpenAIClient

        client = OpenAIClient(api_token=api_token)
        result = client.chat_completions(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in one word."}],
        )
        assert "choices" in result
        assert len(result["choices"]) > 0

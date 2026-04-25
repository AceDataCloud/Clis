"""Tests for output formatting."""

import pytest

from openai_cli.core.output import (
    CHAT_MODELS,
    DEFAULT_CHAT_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_IMAGE_MODEL,
    DEFAULT_RESPONSES_MODEL,
    EMBEDDING_MODELS,
    IMAGE_MODELS,
    RESPONSES_MODELS,
    print_chat_result,
    print_embed_result,
    print_image_result,
    print_models,
)


class TestModelLists:
    """Tests for model list constants."""

    def test_chat_models_contains_gpt54(self):
        assert "gpt-5.4" in CHAT_MODELS

    def test_chat_models_contains_gpt4o(self):
        assert "gpt-4o" in CHAT_MODELS

    def test_chat_models_contains_gpt4o_mini(self):
        assert "gpt-4o-mini" in CHAT_MODELS

    def test_chat_models_contains_o_series(self):
        assert "o1" in CHAT_MODELS
        assert "o3" in CHAT_MODELS
        assert "o4-mini" in CHAT_MODELS

    def test_responses_models_contains_gpt54(self):
        assert "gpt-5.4" in RESPONSES_MODELS

    def test_embedding_models(self):
        assert "text-embedding-3-small" in EMBEDDING_MODELS
        assert "text-embedding-3-large" in EMBEDDING_MODELS
        assert "text-embedding-ada-002" in EMBEDDING_MODELS

    def test_image_models(self):
        assert "dall-e-3" in IMAGE_MODELS
        assert "gpt-image-1" in IMAGE_MODELS

    def test_default_models(self):
        assert DEFAULT_CHAT_MODEL in CHAT_MODELS
        assert DEFAULT_EMBEDDING_MODEL in EMBEDDING_MODELS
        assert DEFAULT_IMAGE_MODEL in IMAGE_MODELS
        assert DEFAULT_RESPONSES_MODEL in RESPONSES_MODELS


class TestPrintFunctions:
    """Tests for print formatting functions."""

    def test_print_chat_result(self, capsys):
        data = {
            "model": "gpt-4o-mini",
            "choices": [
                {
                    "message": {"role": "assistant", "content": "Paris is the capital of France."},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
        }
        print_chat_result(data)

    def test_print_chat_result_no_choices(self, capsys):
        data = {"model": "gpt-4o-mini", "choices": []}
        print_chat_result(data)

    def test_print_embed_result(self, capsys):
        data = {
            "model": "text-embedding-3-small",
            "data": [{"embedding": [0.1, 0.2, 0.3]}],
            "usage": {"total_tokens": 5},
        }
        print_embed_result(data)

    def test_print_image_result_with_url(self, capsys):
        data = {
            "data": [{"url": "https://example.com/img.png", "revised_prompt": "A cat"}]
        }
        print_image_result(data)

    def test_print_image_result_empty(self, capsys):
        data = {"data": []}
        print_image_result(data)

    def test_print_models(self, capsys):
        print_models()

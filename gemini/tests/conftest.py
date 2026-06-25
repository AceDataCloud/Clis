"""Test configuration and fixtures for Gemini CLI."""

import pytest


@pytest.fixture
def mock_chat_response() -> dict:
    return {
        "id": "chatcmpl-test-123",
        "object": "chat.completion",
        "created": 1700000000,
        "model": "gemini-2.5-flash",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "The capital of France is Paris.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
    }


@pytest.fixture
def mock_video_response() -> dict:
    return {
        "data": {
            "id": "task-video-123",
            "state": "succeeded",
            "video_url": "https://example.com/video.mp4",
        }
    }


@pytest.fixture
def mock_task_response() -> dict:
    return {
        "data": {
            "id": "task-video-123",
            "state": "succeeded",
            "video_url": "https://example.com/video.mp4",
        }
    }

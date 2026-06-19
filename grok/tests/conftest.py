"""Pytest configuration and fixtures for Grok CLI tests."""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv(dotenv_path=project_root / ".env")

os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture
def api_token():
    """Get API token from environment for integration tests."""
    token = os.environ.get("ACEDATACLOUD_API_TOKEN", "")
    if not token:
        pytest.skip("ACEDATACLOUD_API_TOKEN not configured for integration tests")
    return token


@pytest.fixture
def mock_chat_response():
    """Mock successful chat completion response."""
    return {
        "id": "chatcmpl-test-123",
        "object": "chat.completion",
        "created": 1700000000,
        "model": "grok-4",
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
def mock_video_response():
    """Mock successful video generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": {
            "task_id": "test-task-123",
            "status": "done",
            "video_url": "https://cdn.example.com/test-video.mp4",
        },
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "test-task-123",
        "trace_id": "test-trace-456",
        "request": {
            "model": "grok-imagine-video",
            "prompt": "A sunset",
        },
        "response": {
            "success": True,
            "data": {
                "task_id": "test-task-123",
                "status": "done",
                "video_url": "https://cdn.example.com/test-video.mp4",
            },
        },
    }

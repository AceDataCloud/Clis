"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file for tests
load_dotenv(dotenv_path=project_root / ".env")

# Set default log level for tests
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
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "model": "claude-3-5-haiku-20241022",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Paris is the capital of France.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 10,
            "total_tokens": 25,
        },
    }


@pytest.fixture
def mock_messages_response():
    """Mock successful Claude Messages API response."""
    return {
        "id": "msg-abc123",
        "type": "message",
        "role": "assistant",
        "model": "claude-3-5-haiku-20241022",
        "content": [
            {
                "type": "text",
                "text": "Paris is the capital of France.",
            }
        ],
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 15,
            "output_tokens": 10,
        },
    }


@pytest.fixture
def mock_count_tokens_response():
    """Mock successful token count response."""
    return {
        "input_tokens": 15,
    }


@pytest.fixture
def mock_queued_response():
    """Mock async/queued response."""
    return {
        "task_id": "task-xyz789",
        "trace_id": "trace-abc123",
    }

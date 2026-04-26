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
        "model": "gpt-4o-mini",
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
def mock_embedding_response():
    """Mock successful embedding response."""
    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "index": 0,
                "embedding": [0.1, 0.2, 0.3, 0.4, 0.5],
            }
        ],
        "model": "text-embedding-3-small",
        "usage": {
            "prompt_tokens": 5,
            "total_tokens": 5,
        },
    }


@pytest.fixture
def mock_image_response():
    """Mock successful image generation response."""
    return {
        "created": 1714000000,
        "data": [
            {
                "url": "https://example.com/generated-image.png",
                "revised_prompt": "A beautiful sunset over mountains",
            }
        ],
    }


@pytest.fixture
def mock_response_api_response():
    """Mock successful Responses API response."""
    return {
        "id": "resp-abc123",
        "object": "response",
        "model": "gpt-4o-mini",
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": "The answer is 42.",
                    }
                ],
            }
        ],
        "usage": {
            "input_tokens": 10,
            "output_tokens": 5,
            "total_tokens": 15,
        },
    }


@pytest.fixture
def mock_queued_response():
    """Mock async/queued response."""
    return {
        "task_id": "task-xyz789",
        "trace_id": "trace-abc123",
    }


@pytest.fixture
def mock_task_response():
    """Mock Tasks API single-task retrieve response."""
    return {
        "_id": "67a1b2c3d4e5f6a7b8c9d0e1",
        "id": "7489df4c-ef03-4de0-b598-e9a590793434",
        "trace_id": "my-custom-trace-001",
        "type": "images_generations",
        "application_id": "9dec7b2a-1cad-41ff-8536-d4ddaf2525d4",
        "user_id": "5d8e7f6a-1234-4abc-9def-0123456789ab",
        "created_at": 1763142607.967,
        "finished_at": 1763142637.404,
        "duration": 29.437,
        "request": {"model": "gpt-image-1", "prompt": "A cat on a table"},
        "response": {
            "created": 1763142637,
            "data": [{"url": "https://example.com/result.png"}],
            "success": True,
        },
    }


@pytest.fixture
def mock_tasks_batch_response():
    """Mock Tasks API retrieve_batch response."""
    return {
        "items": [
            {
                "id": "7489df4c-ef03-4de0-b598-e9a590793434",
                "trace_id": "my-trace-001",
                "type": "images_generations",
                "created_at": 1763142607.967,
                "finished_at": 1763142637.404,
                "response": {"data": [{"url": "https://example.com/result.png"}]},
            }
        ],
        "count": 1,
    }

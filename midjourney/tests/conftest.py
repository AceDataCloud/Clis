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
def mock_imagine_response():
    """Mock successful imagine response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "id": "image-id-1",
                "state": "succeeded",
                "image_url": "https://cdn.example.com/test-image.png",
                "created_at": "2025-01-21T00:00:00.000Z",
            }
        ],
    }


@pytest.fixture
def mock_edits_response():
    """Mock successful edits response."""
    return {
        "success": True,
        "task_id": "test-edits-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "id": "image-id-2",
                "state": "succeeded",
                "image_url": "https://cdn.example.com/test-edited-image.png",
                "created_at": "2025-01-21T00:00:00.000Z",
            }
        ],
    }


@pytest.fixture
def mock_videos_response():
    """Mock successful videos response."""
    return {
        "success": True,
        "task_id": "test-videos-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "id": "video-id-1",
                "state": "succeeded",
                "video_url": "https://cdn.example.com/test-video.mp4",
                "created_at": "2025-01-21T00:00:00.000Z",
            }
        ],
    }


@pytest.fixture
def mock_describe_response():
    """Mock successful describe response."""
    return {
        "success": True,
        "task_id": "test-describe-task-123",
        "trace_id": "test-trace-456",
        "data": {
            "descriptions": [
                "A beautiful sunset over the ocean",
                "Warm orange sky with waves crashing on the shore",
            ]
        },
    }


@pytest.fixture
def mock_shorten_response():
    """Mock successful shorten response."""
    return {
        "success": True,
        "task_id": "test-shorten-task-123",
        "trace_id": "test-trace-456",
        "data": {
            "prompts": [
                "sunset ocean",
                "beautiful coastal scene",
            ]
        },
    }


@pytest.fixture
def mock_translate_response():
    """Mock successful translate response."""
    return {
        "success": True,
        "data": {
            "content": "A beautiful sunset over the ocean",
        },
    }


@pytest.fixture
def mock_seed_response():
    """Mock successful seed response."""
    return {
        "success": True,
        "data": {
            "seed": "123456789",
        },
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "success": True,
        "data": [
            {
                "id": "task-123",
                "status": "completed",
                "state": "succeeded",
                "image_url": "https://cdn.example.com/test-image.png",
                "created_at": "2025-01-21T00:00:00.000Z",
            }
        ],
    }


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {
        "success": False,
        "error": {
            "code": "invalid_request",
            "message": "Invalid parameters provided",
        },
    }

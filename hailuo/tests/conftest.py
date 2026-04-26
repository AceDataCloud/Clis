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
def mock_video_response():
    """Mock successful video generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "video_url": "https://cdn.example.com/test-video.mp4",
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "success": True,
        "data": {
            "id": "task-123",
            "status": "completed",
            "state": "succeeded",
            "video_url": "https://cdn.example.com/test-video.mp4",
            "model": "minimax-t2v",
            "created_at": "2026-04-26T00:00:00.000Z",
        },
    }


@pytest.fixture
def mock_tasks_batch_response():
    """Mock batch task query response."""
    return {
        "success": True,
        "data": [
            {
                "id": "task-123",
                "status": "completed",
                "state": "succeeded",
                "video_url": "https://cdn.example.com/test-video.mp4",
                "model": "minimax-t2v",
                "created_at": "2026-04-26T00:00:00.000Z",
            },
            {
                "id": "task-456",
                "status": "completed",
                "state": "succeeded",
                "video_url": "https://cdn.example.com/test-video2.mp4",
                "model": "minimax-t2v",
                "created_at": "2026-04-26T00:00:00.000Z",
            },
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

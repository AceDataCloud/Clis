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
def mock_audio_response():
    """Mock successful audio generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "id": "audio-id-1",
                "state": "succeeded",
                "title": "Test Song",
                "model_name": "FUZZ-2.0",
                "audio_url": "https://cdn.example.com/test-audio.mp3",
                "created_at": "2026-07-24T00:00:00.000Z",
            }
        ],
    }


@pytest.fixture
def mock_lyrics_response():
    """Mock successful lyrics generation response."""
    return {
        "success": True,
        "data": {
            "text": "[Verse]\nTest lyrics here\n[Chorus]\nTest chorus here",
            "title": "Test Lyrics",
            "status": "complete",
        },
    }


@pytest.fixture
def mock_upload_response():
    """Mock successful audio upload response."""
    return {
        "success": True,
        "data": {
            "audio_id": "uploaded-audio-123",
            "audio_url": "https://cdn.example.com/uploaded.mp3",
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
                "audio_url": "https://cdn.example.com/test-audio.mp3",
                "model_name": "FUZZ-2.0",
                "created_at": "2026-07-24T00:00:00.000Z",
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

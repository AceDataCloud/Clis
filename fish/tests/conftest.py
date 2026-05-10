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
def mock_tts_response():
    """Mock successful TTS synthesis response."""
    return {
        "success": True,
        "audio_url": "https://cdn.example.com/test-audio.mp3",
        "trace_id": "test-trace-456",
    }


@pytest.fixture
def mock_tts_async_response():
    """Mock async TTS synthesis response (with callback_url)."""
    return {
        "success": True,
        "task_id": "test-task-123",
    }


@pytest.fixture
def mock_voice_list_response():
    """Mock voice model list response."""
    return {
        "total": 2,
        "items": [
            {
                "_id": "voice-id-1",
                "title": "Test Voice 1",
                "type": "tts",
                "state": "trained",
                "languages": ["en"],
                "visibility": "public",
            },
            {
                "_id": "voice-id-2",
                "title": "Test Voice 2",
                "type": "tts",
                "state": "trained",
                "languages": ["zh"],
                "visibility": "public",
            },
        ],
    }


@pytest.fixture
def mock_voice_detail_response():
    """Mock single voice model response."""
    return {
        "_id": "voice-id-1",
        "title": "Test Voice 1",
        "type": "tts",
        "state": "trained",
        "train_mode": "fast",
        "visibility": "public",
        "description": "A test voice model.",
        "languages": ["en"],
        "tags": ["podcast"],
        "created_at": "2026-01-01T00:00:00.000Z",
        "updated_at": "2026-01-02T00:00:00.000Z",
        "author": {"name": "Test Author"},
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
                "created_at": "2026-01-01T00:00:00.000Z",
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

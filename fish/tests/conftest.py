"""Pytest configuration and fixtures for Fish CLI tests."""

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
def mock_tts_response():
    """Mock successful TTS generation response."""
    return {
        "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3",
        "latency_ms": 1234,
    }


@pytest.fixture
def mock_tts_async_response():
    """Mock async TTS submission response."""
    return {
        "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
        "started_at": "2025-05-09T12:34:56.789Z",
    }


@pytest.fixture
def mock_models_response():
    """Mock fish models list response."""
    return {
        "items": [
            {
                "_id": "d7900c21663f485ab63ebdb7e5905036",
                "title": "My Cloned Voice",
                "description": "A test voice",
                "type": "tts",
                "state": "trained",
                "tags": [],
                "languages": ["zh", "en"],
                "visibility": "private",
                "created_at": "2025-05-09T12:34:56.789Z",
                "updated_at": "2025-05-09T12:34:56.789Z",
            }
        ],
        "total": 1,
    }


@pytest.fixture
def mock_model_response():
    """Mock single fish model response."""
    return {
        "_id": "d7900c21663f485ab63ebdb7e5905036",
        "title": "My Cloned Voice",
        "description": "A test voice",
        "type": "tts",
        "state": "trained",
        "train_mode": "fast",
        "tags": [],
        "languages": ["zh", "en"],
        "visibility": "private",
        "created_at": "2025-05-09T12:34:56.789Z",
        "updated_at": "2025-05-09T12:34:56.789Z",
        "like_count": 0,
        "mark_count": 0,
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "_id": "68cfad98550a4144a5476a92",
        "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
        "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
        "request": {
            "action": "speech",
            "text": "Hello world",
        },
        "response": {
            "success": True,
            "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
            "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
            "data": [
                {
                    "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
                }
            ],
        },
    }


@pytest.fixture
def mock_tasks_batch_response():
    """Mock batch task query response."""
    task = {
        "_id": "68cfad98550a4144a5476a92",
        "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
        "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
        "request": {"action": "speech", "text": "Hello world"},
        "response": {
            "success": True,
            "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
            "data": [
                {
                    "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
                }
            ],
        },
    }
    return {"items": [task, task], "count": 2}

"""Pytest configuration and fixtures for Dreamina CLI tests."""

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
def mock_video_response():
    """Mock successful video generation response."""
    return {
        "success": True,
        "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
        "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
        "data": {
            "task_id": "362b4fed67bd11f1ad1100163e57d510",
            "status": "done",
            "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
            "image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
            "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav",
        },
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "362b4fed-67bd-11f1-ad11-00163e57d510",
        "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
        "request": {
            "model": "omnihuman-1.5",
            "image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
            "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav",
        },
        "response": {
            "success": True,
            "data": {
                "task_id": "362b4fed67bd11f1ad1100163e57d510",
                "status": "done",
                "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
                "image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
                "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav",
            },
        },
    }

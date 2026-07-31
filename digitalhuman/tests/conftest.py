"""Pytest configuration and fixtures for Digital Human CLI tests."""

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
        "task_id": "task_49af42c410c24f04ad416b28af55d237",
        "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
        "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
        "duration": 17.2,
        "width": 1280,
        "height": 720,
        "engine": "latentsync",
        "state": "succeed",
    }


@pytest.fixture
def mock_voice_response():
    """Mock successful voice cloning response."""
    return {
        "success": True,
        "task_id": "task_voice123",
        "trace_id": "b1234567-89ab-cdef-0123-456789abcdef",
        "voice_id": "f754a190e26c",
        "state": "succeed",
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "success": True,
        "task_id": "task_49af42c410c24f04ad416b28af55d237",
        "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
        "state": "succeed",
        "progress": 100,
        "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
        "duration": 17.2,
        "width": 1280,
        "height": 720,
        "engine": "latentsync",
    }

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
    """Mock successful image generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "image_url": "https://cdn.example.com/test-image.png",
        "image_id": "img-789",
        "image_width": 1024,
        "image_height": 1024,
        "actions": ["upscale1", "upscale2", "upscale3", "upscale4"],
    }


@pytest.fixture
def mock_edit_response():
    """Mock successful edit response."""
    return {
        "success": True,
        "task_id": "test-edit-123",
        "trace_id": "test-trace-edit",
        "image_url": "https://cdn.example.com/edited-image.png",
        "image_id": "edit-789",
        "image_width": 1024,
        "image_height": 1024,
    }


@pytest.fixture
def mock_describe_response():
    """Mock successful describe response."""
    return {
        "success": True,
        "descriptions": [
            "A detailed painting of a sunset --ar 16:9",
            "Warm colors landscape with mountains --ar 16:9",
            "Golden hour photography of nature --ar 16:9",
            "Impressionist style countryside view --ar 16:9",
        ],
    }


@pytest.fixture
def mock_translate_response():
    """Mock successful translate response."""
    return {
        "success": True,
        "translated_content": "A cat sitting on a table",
    }


@pytest.fixture
def mock_video_response():
    """Mock successful video generation response."""
    return {
        "success": True,
        "task_id": "test-video-123",
        "trace_id": "test-trace-vid",
        "cover_image_url": "https://cdn.example.com/cover.jpg",
        "video_urls": [
            "https://cdn.example.com/video1.mp4",
            "https://cdn.example.com/video2.mp4",
        ],
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "success": True,
        "task_id": "task-123",
        "image_url": "https://cdn.example.com/result.png",
        "image_id": "img-result",
        "image_width": 1024,
        "image_height": 1024,
        "actions": ["upscale_2x", "variation_subtle"],
    }


@pytest.fixture
def mock_seed_response():
    """Mock seed response."""
    return {
        "success": True,
        "seed": 1234567890,
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

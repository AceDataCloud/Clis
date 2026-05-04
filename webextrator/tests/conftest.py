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
def mock_extract_response():
    """Mock successful extract response."""
    return {
        "success": True,
        "task_id": "extract-task-123",
        "trace_id": "extract-trace-456",
        "started_at": "2025-05-02T10:30:00.123Z",
        "finished_at": "2025-05-02T10:30:08.789Z",
        "elapsed": 8.666,
        "data": {
            "kind": "extract",
            "url": "https://www.amazon.com/dp/B0C1234567",
            "contentType": "product",
            "title": "Acme Widget",
            "description": "A widget that does things.",
            "siteName": "Amazon.com",
        },
    }


@pytest.fixture
def mock_render_response():
    """Mock successful render response."""
    return {
        "success": True,
        "task_id": "render-task-123",
        "trace_id": "render-trace-456",
        "started_at": "2025-05-02T10:30:00.123Z",
        "finished_at": "2025-05-02T10:30:05.456Z",
        "elapsed": 5.333,
        "data": {
            "kind": "render",
            "url": "https://example.com",
            "finalUrl": "https://example.com/",
            "title": "Example Domain",
            "status": 200,
            "html": "<!DOCTYPE html><html>...</html>",
        },
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "extract-task-123",
        "trace_id": "extract-trace-456",
        "task_id": "extract-task-123",
        "type": "extract",
        "started_at": "2025-05-02T10:30:00.123Z",
        "finished_at": "2025-05-02T10:30:08.789Z",
        "elapsed": 8.666,
        "request": {"url": "https://example.com"},
        "response": {"kind": "extract", "title": "Example"},
    }


@pytest.fixture
def mock_task_batch_response():
    """Mock task batch query response."""
    return {
        "items": [
            {
                "id": "task-1",
                "trace_id": "trace-1",
                "type": "render",
                "started_at": "2025-05-02T10:30:00.123Z",
            },
            {
                "id": "task-2",
                "trace_id": "trace-2",
                "type": "extract",
                "started_at": "2025-05-02T10:31:00.000Z",
            },
        ],
        "count": 2,
    }


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {
        "success": False,
        "error": {
            "code": "bad_request",
            "message": "url is required",
        },
    }

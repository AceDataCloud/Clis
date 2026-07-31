"""Pytest configuration and fixtures for DrawAI CLI tests."""

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
def mock_headshot_response():
    """Mock successful headshot generation response."""
    return {
        "success": True,
        "task_id": "abc123-def456",
        "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
        "state": "succeed",
        "images": ["https://cdn.acedata.cloud/headshot1.jpg"],
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "abc123-def456",
        "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
        "state": "succeed",
        "progress": 100,
    }

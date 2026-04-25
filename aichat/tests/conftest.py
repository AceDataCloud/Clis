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
def mock_chat_response():
    """Mock successful chat response."""
    return {
        "id": "64a67fff-61dc-4801-8339-2c69334c61d6",
        "answer": "I am a highly intelligent question answering AI.",
    }


@pytest.fixture
def mock_empty_response():
    """Mock empty response."""
    return {}


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {
        "error": {
            "code": "invalid_request",
            "message": "Invalid parameters provided",
        },
    }

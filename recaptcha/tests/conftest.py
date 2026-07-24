"""Pytest configuration and fixtures for reCAPTCHA CLI tests."""

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
def mock_recognition_response():
    """Mock successful reCAPTCHA recognition response."""
    return {
        "solution": {
            "label": "Select all cars",
            "confidences": [True, False, True],
        }
    }


@pytest.fixture
def mock_recognition_async_response():
    """Mock async reCAPTCHA recognition submission response."""
    return {
        "task_id": "3a8b1c2d-4e5f-6789-abcd-ef0123456789",
    }


@pytest.fixture
def mock_token_response():
    """Mock successful reCAPTCHA token response."""
    return {
        "token": "03AGdBq25SxXT-pmSeBXjzScW-EiocHwwpwqtk1QBB3nDoQTQ1234567890",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }


@pytest.fixture
def mock_token_async_response():
    """Mock async reCAPTCHA token submission response."""
    return {
        "task_id": "3a8b1c2d-4e5f-6789-abcd-ef0123456789",
    }

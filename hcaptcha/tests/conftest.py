"""Pytest configuration and fixtures for hCaptcha CLI tests."""

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
    """Mock successful hCaptcha recognition response."""
    return {
        "solution": {
            "box": ["565", "140"],
            "label": "Please click the center of the seahorses head",
            "confidences": 0.7175476551055908,
        }
    }


@pytest.fixture
def mock_recognition_async_response():
    """Mock async hCaptcha recognition submission response."""
    return {
        "task_id": "3a8b1c2d-4e5f-6789-abcd-ef0123456789",
    }


@pytest.fixture
def mock_token_response():
    """Mock successful hCaptcha token response."""
    return {
        "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test-token",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }


@pytest.fixture
def mock_token_async_response():
    """Mock async hCaptcha token submission response."""
    return {
        "task_id": "3a8b1c2d-4e5f-6789-abcd-ef0123456789",
    }

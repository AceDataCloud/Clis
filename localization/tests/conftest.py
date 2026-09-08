"""Pytest configuration and fixtures for Localization CLI tests."""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

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
def mock_translation_response():
    """Mock successful localization translation response."""
    return {
        "data": {
            "message.clickButton": {
                "message": "请点击按钮以应用",
                "description": "Localization Translate Response 200 Example Data Message Clickbutton",
            }
        },
        "model": "gpt-4",
        "locale": "zh-CN",
    }

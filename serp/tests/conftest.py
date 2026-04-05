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
def mock_search_response():
    """Mock successful web search response."""
    return {
        "organic": [
            {
                "title": "What is Artificial Intelligence?",
                "link": "https://example.com/ai",
                "snippet": "Artificial intelligence is the simulation of human intelligence.",
            },
            {
                "title": "AI Overview",
                "link": "https://example.com/overview",
                "snippet": "A comprehensive overview of AI technologies.",
            },
        ],
        "knowledge_graph": {
            "title": "Artificial Intelligence",
            "description": "A branch of computer science.",
        },
        "people_also_ask": [
            {"question": "What are the types of AI?"},
            {"question": "How does AI work?"},
        ],
        "related_searches": [
            {"query": "machine learning"},
            {"query": "deep learning"},
        ],
    }


@pytest.fixture
def mock_images_response():
    """Mock image search response."""
    return {
        "images": [
            {
                "title": "Sunset Photo",
                "original": "https://example.com/sunset.jpg",
                "link": "https://example.com/sunset-page",
            },
        ],
    }


@pytest.fixture
def mock_news_response():
    """Mock news search response."""
    return {
        "news": [
            {
                "title": "AI Breakthrough in 2025",
                "source": "TechCrunch",
                "date": "2 hours ago",
                "link": "https://example.com/news/ai",
            },
        ],
    }


@pytest.fixture
def mock_empty_response():
    """Mock empty search response."""
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

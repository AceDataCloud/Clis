"""Test configuration and fixtures for WebExtrator CLI."""

import pytest


@pytest.fixture
def mock_extract_response() -> dict:
    return {
        "success": True,
        "task_id": "550e8400-e29b-41d4-a716-446655440000",
        "trace_id": "550e8400-e29b-41d4-a716-446655440001",
        "started_at": "2025-05-02T10:30:00.123Z",
        "finished_at": "2025-05-02T10:30:08.789Z",
        "elapsed": 8.666,
        "data": {
            "kind": "extract",
            "url": "https://www.amazon.com/dp/B0C1234567",
            "contentType": "product",
            "title": "Acme Widget",
            "description": "A widget that does things.",
        },
    }


@pytest.fixture
def mock_render_response() -> dict:
    return {
        "success": True,
        "task_id": "550e8400-e29b-41d4-a716-446655440002",
        "trace_id": "550e8400-e29b-41d4-a716-446655440003",
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
def mock_task_response() -> dict:
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "task_id": "550e8400-e29b-41d4-a716-446655440000",
        "trace_id": "550e8400-e29b-41d4-a716-446655440001",
        "type": "extract",
        "started_at": "2025-05-02T10:30:00.123Z",
        "finished_at": "2025-05-02T10:30:08.789Z",
        "elapsed": 8.666,
    }

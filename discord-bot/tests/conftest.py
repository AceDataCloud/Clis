"""Test configuration and fixtures for Discord Bot CLI."""

import pytest

BASE_URL = "https://discord-bot-test.app.acedata.cloud"
TOKEN = "test-token"


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def mock_health_response() -> dict:
    return {"status": "ok", "gateway_ready": True}


@pytest.fixture
def mock_whoami_response() -> dict:
    return {
        "data": {
            "id": "111222333444555666",
            "username": "testuser",
            "discriminator": "0",
            "global_name": "Test User",
        }
    }


@pytest.fixture
def mock_guilds_response() -> dict:
    return {
        "data": [
            {"id": "1234567890", "name": "My Server"},
            {"id": "9876543210", "name": "Another Server"},
        ]
    }


@pytest.fixture
def mock_channels_response() -> dict:
    return {
        "data": [
            {"id": "111000111", "name": "general", "type": 0},
            {"id": "222000222", "name": "announcements", "type": 0},
        ]
    }


@pytest.fixture
def mock_members_response() -> dict:
    return {
        "data": [
            {"user": {"id": "111222333", "username": "alice"}, "nick": None},
            {"user": {"id": "444555666", "username": "bob"}, "nick": "Bobby"},
        ]
    }


@pytest.fixture
def mock_message_response() -> dict:
    return {
        "data": {
            "id": "9876543210",
            "channel_id": "1234567890",
            "content": "Hello!",
            "timestamp": "2026-08-01T00:00:00.000Z",
        }
    }


@pytest.fixture
def mock_messages_response() -> dict:
    return {
        "data": [
            {
                "id": "9876543210",
                "author": {"username": "alice"},
                "content": "Hello!",
            },
            {
                "id": "9876543211",
                "author": {"username": "bob"},
                "content": "Hi there!",
            },
        ]
    }


@pytest.fixture
def mock_channel_response() -> dict:
    return {"data": {"id": "777888999", "type": 1}}

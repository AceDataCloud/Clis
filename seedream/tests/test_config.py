"""Tests for configuration module."""

import os

from seedream_cli.core.config import Settings


def test_settings_default_values():
    settings = Settings()
    assert settings.api_base_url == "https://api.acedata.cloud"
    assert settings.request_timeout == 1800
    assert settings.default_model == "doubao-seedream-4-0-250828"


def test_settings_from_environment():
    os.environ["ACEDATACLOUD_API_TOKEN"] = "test-token-123"
    os.environ["ACEDATACLOUD_API_BASE_URL"] = "https://custom.api.example.com"
    os.environ["SEEDREAM_REQUEST_TIMEOUT"] = "300"
    os.environ["SEEDREAM_DEFAULT_MODEL"] = "doubao-seedream-4-5-251128"

    try:
        settings = Settings()
        assert settings.api_token == "test-token-123"
        assert settings.api_base_url == "https://custom.api.example.com"
        assert settings.request_timeout == 300
        assert settings.default_model == "doubao-seedream-4-5-251128"
    finally:
        del os.environ["ACEDATACLOUD_API_TOKEN"]
        del os.environ["ACEDATACLOUD_API_BASE_URL"]
        del os.environ["SEEDREAM_REQUEST_TIMEOUT"]
        del os.environ["SEEDREAM_DEFAULT_MODEL"]


def test_settings_is_configured():
    settings = Settings()
    settings.api_token = ""
    assert not settings.is_configured

    settings.api_token = "some-token"
    assert settings.is_configured


def test_settings_validate_missing_token():
    settings = Settings()
    settings.api_token = ""
    try:
        settings.validate()
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "API token not configured" in str(e)


def test_settings_validate_with_token():
    settings = Settings()
    settings.api_token = "valid-token"
    settings.validate()  # Should not raise

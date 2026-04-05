"""Tests for configuration module."""

import os

from wan_cli.core.config import Settings


def test_settings_default_values():
    settings = Settings()
    assert settings.api_base_url == "https://api.acedata.cloud"
    assert settings.request_timeout == 1800
    assert settings.default_model == "wan2.6-t2v"


def test_settings_from_environment():
    os.environ["ACEDATACLOUD_API_TOKEN"] = "test-token-123"
    os.environ["ACEDATACLOUD_API_BASE_URL"] = "https://custom.api.example.com"
    os.environ["WAN_REQUEST_TIMEOUT"] = "300"
    os.environ["WAN_DEFAULT_MODEL"] = "wan2.6-i2v"

    try:
        settings = Settings()
        assert settings.api_token == "test-token-123"
        assert settings.api_base_url == "https://custom.api.example.com"
        assert settings.request_timeout == 300
        assert settings.default_model == "wan2.6-i2v"
    finally:
        del os.environ["ACEDATACLOUD_API_TOKEN"]
        del os.environ["ACEDATACLOUD_API_BASE_URL"]
        del os.environ["WAN_REQUEST_TIMEOUT"]
        del os.environ["WAN_DEFAULT_MODEL"]


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

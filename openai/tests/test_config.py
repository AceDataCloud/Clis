"""Tests for configuration."""

import os

import pytest

from openai_cli.core.config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_api_base_url(self):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"

    def test_custom_api_base_url(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_BASE_URL", "https://custom.api.example.com")
        settings = Settings()
        assert settings.api_base_url == "https://custom.api.example.com"

    def test_api_token_from_env(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "test-token-123")
        settings = Settings()
        assert settings.api_token == "test-token-123"

    def test_default_timeout(self):
        settings = Settings()
        assert settings.request_timeout == 60.0

    def test_custom_timeout(self, monkeypatch):
        monkeypatch.setenv("OPENAI_REQUEST_TIMEOUT", "120")
        settings = Settings()
        assert settings.request_timeout == 120.0

    def test_is_configured_with_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "some-token")
        settings = Settings()
        assert settings.is_configured is True

    def test_is_not_configured_without_token(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        settings = Settings()
        assert settings.is_configured is False

    def test_validate_raises_without_token(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        settings = Settings()
        with pytest.raises(ValueError, match="API token not configured"):
            settings.validate()

    def test_validate_passes_with_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "my-token")
        settings = Settings()
        settings.validate()  # Should not raise

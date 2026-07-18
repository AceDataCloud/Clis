"""Tests for Kimi CLI configuration."""


import pytest

from kimi_cli.core.config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_base_url(self):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"

    def test_api_token_from_env(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "env-token-123")
        settings = Settings()
        assert settings.api_token == "env-token-123"

    def test_is_configured_with_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "some-token")
        settings = Settings()
        assert settings.is_configured is True

    def test_is_configured_without_token(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        settings = Settings()
        assert settings.is_configured is False

    def test_validate_raises_without_token(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        settings = Settings()
        with pytest.raises(ValueError, match="API token not configured"):
            settings.validate()

    def test_validate_passes_with_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "valid-token")
        settings = Settings()
        settings.validate()  # Should not raise

    def test_timeout_from_env(self, monkeypatch):
        monkeypatch.setenv("KIMI_REQUEST_TIMEOUT", "60")
        settings = Settings()
        assert settings.request_timeout == 60.0

"""Tests for configuration."""


import pytest

from claude_cli.core.config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_base_url(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_BASE_URL", raising=False)
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"

    def test_custom_base_url(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_BASE_URL", "https://custom.example.com")
        settings = Settings()
        assert settings.api_base_url == "https://custom.example.com"

    def test_api_token_from_env(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "my-test-token")
        settings = Settings()
        assert settings.api_token == "my-test-token"

    def test_is_configured_true(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "my-test-token")
        settings = Settings()
        assert settings.is_configured is True

    def test_is_configured_false(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        settings = Settings()
        assert settings.is_configured is False

    def test_validate_raises_without_token(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        settings = Settings()
        with pytest.raises(ValueError, match="API token not configured"):
            settings.validate()

    def test_validate_passes_with_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "my-test-token")
        settings = Settings()
        settings.validate()  # Should not raise

    def test_default_timeout(self, monkeypatch):
        monkeypatch.delenv("CLAUDE_REQUEST_TIMEOUT", raising=False)
        settings = Settings()
        assert settings.request_timeout == 30.0

    def test_custom_timeout(self, monkeypatch):
        monkeypatch.setenv("CLAUDE_REQUEST_TIMEOUT", "60")
        settings = Settings()
        assert settings.request_timeout == 60.0

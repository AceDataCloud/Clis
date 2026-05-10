"""Tests for configuration."""

import pytest

from fish_cli.core.config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_defaults(self):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"
        assert settings.request_timeout == 300.0
        assert settings.default_model == "s2-pro"

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "env-token")
        monkeypatch.setenv("ACEDATACLOUD_API_BASE_URL", "https://custom.api")
        monkeypatch.setenv("FISH_DEFAULT_MODEL", "s1")
        monkeypatch.setenv("FISH_REQUEST_TIMEOUT", "60")
        settings = Settings()
        assert settings.api_token == "env-token"
        assert settings.api_base_url == "https://custom.api"
        assert settings.default_model == "s1"
        assert settings.request_timeout == 60.0

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

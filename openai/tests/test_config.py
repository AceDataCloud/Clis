"""Tests for configuration."""


import pytest

from openai_cli.core.config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_base_url(self):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"

    def test_token_from_env(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "my-test-token")
        settings = Settings()
        assert settings.api_token == "my-test-token"

    def test_is_configured_false_when_no_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "")
        settings = Settings()
        assert not settings.is_configured

    def test_is_configured_true_when_token_set(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "some-token")
        settings = Settings()
        assert settings.is_configured

    def test_validate_raises_when_no_token(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "")
        settings = Settings()
        with pytest.raises(ValueError, match="API token not configured"):
            settings.validate()

    def test_custom_base_url(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_BASE_URL", "https://custom.example.com")
        settings = Settings()
        assert settings.api_base_url == "https://custom.example.com"

    def test_custom_timeout(self, monkeypatch):
        monkeypatch.setenv("OPENAI_REQUEST_TIMEOUT", "60")
        settings = Settings()
        assert settings.request_timeout == 60.0

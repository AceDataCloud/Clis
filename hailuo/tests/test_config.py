"""Tests for Hailuo CLI configuration."""

import os

import pytest

from hailuo_cli.core.config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_base_url(self):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"

    def test_token_from_env(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "env-token")
        settings = Settings()
        assert settings.api_token == "env-token"

    def test_is_configured_false(self):
        settings = Settings()
        settings.api_token = ""
        assert settings.is_configured is False

    def test_is_configured_true(self):
        settings = Settings()
        settings.api_token = "some-token"
        assert settings.is_configured is True

    def test_validate_raises_without_token(self):
        settings = Settings()
        settings.api_token = ""
        with pytest.raises(ValueError, match="API token not configured"):
            settings.validate()

    def test_validate_passes_with_token(self):
        settings = Settings()
        settings.api_token = "valid-token"
        settings.validate()  # Should not raise

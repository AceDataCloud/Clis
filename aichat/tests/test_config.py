"""Tests for configuration."""

import os

import pytest

from aichat_cli.core.config import Settings


class TestSettings:
    """Tests for Settings dataclass."""

    def test_defaults(self, monkeypatch):
        monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
        monkeypatch.delenv("ACEDATACLOUD_API_BASE_URL", raising=False)
        monkeypatch.delenv("AICHAT_REQUEST_TIMEOUT", raising=False)
        s = Settings()
        assert s.api_base_url == "https://api.acedata.cloud"
        assert s.api_token == ""
        assert s.request_timeout == 30.0

    def test_custom_values(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "my-token")
        monkeypatch.setenv("ACEDATACLOUD_API_BASE_URL", "https://custom.api")
        monkeypatch.setenv("AICHAT_REQUEST_TIMEOUT", "60")
        s = Settings()
        assert s.api_token == "my-token"
        assert s.api_base_url == "https://custom.api"
        assert s.request_timeout == 60.0

    def test_is_configured_with_token(self):
        s = Settings()
        s.api_token = "some-token"
        assert s.is_configured is True

    def test_is_configured_without_token(self):
        s = Settings()
        s.api_token = ""
        assert s.is_configured is False

    def test_validate_raises_without_token(self):
        s = Settings()
        s.api_token = ""
        with pytest.raises(ValueError, match="API token not configured"):
            s.validate()

    def test_validate_passes_with_token(self):
        s = Settings()
        s.api_token = "valid-token"
        s.validate()  # Should not raise

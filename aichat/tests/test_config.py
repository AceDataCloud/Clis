"""Tests for configuration."""

import os

import pytest

from aichat_cli.core.config import Settings


class TestSettings:
    """Tests for Settings dataclass."""

    def test_default_base_url(self):
        s = Settings()
        assert s.api_base_url == "https://api.acedata.cloud"

    def test_api_token_from_env(self, monkeypatch):
        monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "env-token")
        s = Settings()
        assert s.api_token == "env-token"

    def test_is_configured_true(self):
        s = Settings()
        s.api_token = "some-token"
        assert s.is_configured is True

    def test_is_configured_false(self):
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
        s.validate()  # should not raise

    def test_request_timeout_default(self):
        s = Settings()
        assert s.request_timeout == 30.0

    def test_request_timeout_from_env(self, monkeypatch):
        monkeypatch.setenv("AICHAT_REQUEST_TIMEOUT", "60")
        s = Settings()
        assert s.request_timeout == 60.0

"""Tests for configuration."""

import os
from unittest.mock import patch

from adc_cli.core.config import (
    Settings,
    load_token_from_config,
    save_token_to_config,
)


class TestSettings:
    """Tests for Settings."""

    def test_default_values(self):
        with patch.dict(os.environ, {}, clear=True):
            s = Settings()
            assert s.api_base_url == "https://api.acedata.cloud"
            assert s.api_token == ""
            assert s.request_timeout == 1800.0

    def test_from_env(self):
        with patch.dict(
            os.environ,
            {
                "ACEDATACLOUD_API_BASE_URL": "https://custom.api",
                "ACEDATACLOUD_API_TOKEN": "env-token",
                "ADC_REQUEST_TIMEOUT": "60",
            },
        ):
            s = Settings()
            assert s.api_base_url == "https://custom.api"
            assert s.api_token == "env-token"
            assert s.request_timeout == 60.0

    def test_is_configured(self):
        s = Settings()
        s.api_token = ""
        assert not s.is_configured
        s.api_token = "some-token"
        assert s.is_configured

    def test_validate_raises_without_token(self):
        s = Settings()
        s.api_token = ""
        import pytest

        with pytest.raises(ValueError, match="API token not configured"):
            s.validate()

    def test_validate_passes_with_token(self):
        s = Settings()
        s.api_token = "valid-token"
        s.validate()  # Should not raise


class TestConfigFile:
    """Tests for config file operations."""

    def test_save_and_load_token(self, tmp_path):
        config_file = tmp_path / "config"
        with (
            patch("adc_cli.core.config.CONFIG_DIR", tmp_path),
            patch("adc_cli.core.config.CONFIG_FILE", config_file),
        ):
            save_token_to_config("my-secret-token")
            assert config_file.exists()
            token = load_token_from_config()
            assert token == "my-secret-token"

    def test_load_token_missing_file(self, tmp_path):
        config_file = tmp_path / "nonexistent" / "config"
        with patch("adc_cli.core.config.CONFIG_FILE", config_file):
            token = load_token_from_config()
            assert token == ""

    def test_save_creates_directory(self, tmp_path):
        nested = tmp_path / "nested" / "dir"
        config_file = nested / "config"
        with (
            patch("adc_cli.core.config.CONFIG_DIR", nested),
            patch("adc_cli.core.config.CONFIG_FILE", config_file),
        ):
            save_token_to_config("token-abc")
            assert nested.exists()
            assert config_file.read_text() == "token=token-abc\n"

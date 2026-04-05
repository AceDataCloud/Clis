"""Configuration management for AceDataCloud CLI."""

import os
from dataclasses import dataclass, field
from pathlib import Path

import click
from dotenv import load_dotenv

load_dotenv()

# Config file location
CONFIG_DIR = Path(click.get_app_dir("adc"))
CONFIG_FILE = CONFIG_DIR / "config"


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    api_base_url: str = field(
        default_factory=lambda: os.environ.get(
            "ACEDATACLOUD_API_BASE_URL", "https://api.acedata.cloud"
        )
    )
    api_token: str = field(default_factory=lambda: os.environ.get("ACEDATACLOUD_API_TOKEN", ""))
    request_timeout: float = field(
        default_factory=lambda: float(os.environ.get("ADC_REQUEST_TIMEOUT", "1800"))
    )

    @property
    def is_configured(self) -> bool:
        """Check if the API token is configured."""
        return bool(self.api_token)

    def validate(self) -> None:
        """Validate configuration. Raises ValueError if API token is missing."""
        if not self.api_token:
            raise ValueError(
                "API token not configured. "
                "Set ACEDATACLOUD_API_TOKEN environment variable or run 'adc auth login'."
            )


def load_token_from_config() -> str:
    """Load API token from config file if it exists."""
    if CONFIG_FILE.exists():
        for line in CONFIG_FILE.read_text().splitlines():
            if line.startswith("token="):
                return line.split("=", 1)[1].strip()
    return ""


def save_token_to_config(token: str) -> None:
    """Save API token to config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(f"token={token}\n")


def get_settings() -> Settings:
    """Get settings, falling back to config file for token."""
    s = Settings()
    if not s.api_token:
        s.api_token = load_token_from_config()
    return s


settings = get_settings()

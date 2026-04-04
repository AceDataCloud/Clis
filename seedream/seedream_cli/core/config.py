"""Configuration management for Seedream CLI."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


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
        default_factory=lambda: float(os.environ.get("SEEDREAM_REQUEST_TIMEOUT", "1800"))
    )
    default_model: str = field(
        default_factory=lambda: os.environ.get(
            "SEEDREAM_DEFAULT_MODEL", "doubao-seedream-4-0-250828"
        )
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
                "Set ACEDATACLOUD_API_TOKEN environment variable or use --token option."
            )


settings = Settings()

"""Configuration management for Discord Bot CLI."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    base_url: str = field(
        default_factory=lambda: os.environ.get("DISCORD_BOT_BASE_URL", "")
    )
    token: str = field(default_factory=lambda: os.environ.get("DISCORD_BOT_TOKEN", ""))
    request_timeout: float = field(
        default_factory=lambda: float(os.environ.get("DISCORD_BOT_REQUEST_TIMEOUT", "30"))
    )

    @property
    def is_configured(self) -> bool:
        """Check if the service is configured."""
        return bool(self.base_url and self.token)

    def validate(self) -> None:
        """Validate configuration. Raises ValueError if required fields are missing."""
        if not self.base_url:
            raise ValueError(
                "Discord Bot base URL not configured. "
                "Set DISCORD_BOT_BASE_URL environment variable or use --base-url option."
            )
        if not self.token:
            raise ValueError(
                "Discord Bot token not configured. "
                "Set DISCORD_BOT_TOKEN environment variable or use --token option."
            )


settings = Settings()

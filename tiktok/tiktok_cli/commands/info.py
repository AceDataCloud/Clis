"""Info and utility commands."""

import click

from tiktok_cli.core.config import settings
from tiktok_cli.core.output import print_config


@click.command()
def config() -> None:
    """Show current configuration."""
    print_config("TikTok CLI Configuration", settings)

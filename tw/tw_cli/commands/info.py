"""Info and utility commands."""

import click

from tw_cli.core.config import settings
from tw_cli.core.output import print_config


@click.command()
def config() -> None:
    """Show current configuration."""
    print_config("Twitter CLI Configuration", settings)

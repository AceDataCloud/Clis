"""Info and utility commands."""

import click

from face_change_cli.core.config import settings
from face_change_cli.core.output import print_config


@click.command()
def config() -> None:
    """Show current configuration."""
    print_config("Face Change CLI Configuration", settings)

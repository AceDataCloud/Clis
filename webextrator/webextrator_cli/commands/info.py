"""Info and utility commands."""

import click

from webextrator_cli.core.config import settings
from webextrator_cli.core.output import console


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="WebExtrator CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

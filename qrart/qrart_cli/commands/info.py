"""Info and utility commands for QRArt CLI."""

import click

from qrart_cli.core.output import console, print_presets


@click.command()
def presets() -> None:
    """List available style presets."""
    print_presets()


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    from qrart_cli.core.config import settings

    table = Table(title="Configuration", show_header=False)
    table.add_column("Key", style="bold")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}...{settings.api_token[-4:]}"
        if len(settings.api_token) > 12
        else ("(not set)" if not settings.api_token else settings.api_token),
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

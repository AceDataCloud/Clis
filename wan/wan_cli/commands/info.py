"""Info and utility commands."""

import click

from wan_cli.core.config import settings
from wan_cli.core.output import RESOLUTIONS, SHOT_TYPES, console, print_models


@click.command()
def models() -> None:
    """List available Wan models."""
    print_models()


@click.command()
def resolutions() -> None:
    """List available video resolutions."""
    from rich.table import Table

    table = Table(title="Available Resolutions")
    table.add_column("Resolution", style="bold cyan")
    table.add_column("Description")

    descriptions = {
        "480P": "Standard definition",
        "720P": "High definition",
        "1080P": "Full high definition",
    }

    for res in RESOLUTIONS:
        table.add_row(res, descriptions.get(res, ""))

    console.print(table)


@click.command("shot-types")
def shot_types() -> None:
    """List available shot types."""
    from rich.table import Table

    table = Table(title="Available Shot Types")
    table.add_column("Type", style="bold cyan")
    table.add_column("Description")

    descriptions = {
        "single": "Single continuous shot",
        "multi": "Multiple switching shots",
    }

    for shot_type in SHOT_TYPES:
        table.add_row(shot_type, descriptions.get(shot_type, ""))

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Wan CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token", f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]"
    )
    table.add_row("Default Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

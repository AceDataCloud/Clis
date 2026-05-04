"""Info and utility commands."""

import click

from kling_cli.core.config import settings
from kling_cli.core.output import ASPECT_RATIOS, console, print_models


@click.command()
def models() -> None:
    """List available Kling models."""
    print_models()


@click.command("aspect-ratios")
def aspect_ratios() -> None:
    """List available aspect ratios."""
    from rich.table import Table

    table = Table(title="Available Aspect Ratios")
    table.add_column("Ratio", style="bold cyan")
    table.add_column("Orientation")

    for ratio in ASPECT_RATIOS:
        w, h = ratio.split(":")
        if int(w) > int(h):
            orientation = "Landscape"
        elif int(w) < int(h):
            orientation = "Portrait"
        else:
            orientation = "Square"
        table.add_row(ratio, orientation)

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Kling CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

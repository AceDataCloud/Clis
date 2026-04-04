"""Info and utility commands."""

import click

from seedance_cli.core.config import settings
from seedance_cli.core.output import ASPECT_RATIOS, RESOLUTIONS, console, print_models


@click.command()
def models() -> None:
    """List available Seedance models."""
    print_models()


@click.command("aspect-ratios")
def aspect_ratios() -> None:
    """List available aspect ratios."""
    from rich.table import Table

    table = Table(title="Available Aspect Ratios")
    table.add_column("Ratio", style="bold cyan")
    table.add_column("Orientation")

    for ratio in ASPECT_RATIOS:
        if ":" in ratio:
            w, h = ratio.split(":")
            if int(w) > int(h):
                orientation = "Landscape"
            elif int(w) < int(h):
                orientation = "Portrait"
            else:
                orientation = "Square"
        else:
            orientation = "Adaptive"
        table.add_row(ratio, orientation)

    console.print(table)


@click.command()
def resolutions() -> None:
    """List available output resolutions."""
    from rich.table import Table

    table = Table(title="Available Resolutions")
    table.add_column("Resolution", style="bold cyan")
    table.add_column("Description")

    desc_map = {
        "480p": "Standard",
        "720p": "HD",
        "1080p": "Full HD",
        "1K": "Default",
        "2K": "High resolution",
        "4K": "Ultra-high resolution",
    }
    for r in RESOLUTIONS:
        table.add_row(r, desc_map.get(r, r))

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Seedance CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token", f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]"
    )
    table.add_row("Default Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

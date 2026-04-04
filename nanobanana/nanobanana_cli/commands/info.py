"""Info and utility commands."""

import click

from nanobanana_cli.core.config import settings
from nanobanana_cli.core.output import ASPECT_RATIOS, RESOLUTIONS, console, print_models


@click.command()
def models() -> None:
    """List available NanoBanana models."""
    print_models()


@click.command("aspect-ratios")
def aspect_ratios() -> None:
    """List available aspect ratios.

    Examples:

      nanobanana aspect-ratios
    """
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
def resolutions() -> None:
    """List available output resolutions (nano-banana-pro only).

    Examples:

      nanobanana resolutions
    """
    from rich.table import Table

    table = Table(title="Available Resolutions (nano-banana-pro only)")
    table.add_column("Resolution", style="bold cyan")
    table.add_column("Description")

    table.add_row("1K", "Default resolution")
    table.add_row("2K", "High resolution")
    table.add_row("4K", "Ultra-high resolution")

    console.print(table)
    console.print(f"\n[dim]Available resolutions: {', '.join(RESOLUTIONS)}[/dim]")


@click.command()
def config() -> None:
    """Show current configuration.

    Examples:

      nanobanana config
    """
    from rich.table import Table

    table = Table(title="NanoBanana CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token", f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]"
    )
    table.add_row("Default Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

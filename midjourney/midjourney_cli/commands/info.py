"""Info and utility commands."""

import click

from midjourney_cli.core.config import settings
from midjourney_cli.core.output import console, print_modes, print_versions


@click.command()
def modes() -> None:
    """List available generation modes."""
    print_modes()


@click.command()
def versions() -> None:
    """List available Midjourney versions."""
    print_versions()


@click.command()
def actions() -> None:
    """List available transform actions."""
    from rich.table import Table

    table = Table(title="Transform Actions")
    table.add_column("Action", style="bold cyan")
    table.add_column("Category")
    table.add_column("Description")

    rows = [
        ("upscale1-4", "Upscale", "Upscale one of the 4 grid images"),
        ("upscale_2x", "Upscale", "Further upscale by 2x"),
        ("upscale_4x", "Upscale", "Further upscale by 4x"),
        ("variation1-4", "Variation", "Create variations of one grid image"),
        ("variation_subtle", "Variation", "Subtle variations after upscale"),
        ("variation_strong", "Variation", "Strong variations after upscale"),
        ("variation_region", "Variation", "Edit specific region with mask"),
        ("reroll", "Regenerate", "Regenerate all 4 images"),
        ("zoom_out_2x", "Zoom", "Zoom out by 2x"),
        ("zoom_out_1_5x", "Zoom", "Zoom out by 1.5x"),
        ("pan_left/right/up/down", "Pan", "Expand in a direction"),
    ]
    for action, category, desc in rows:
        table.add_row(action, category, desc)

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Midjourney CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

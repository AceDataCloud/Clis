"""Info and utility commands."""

import click

from gemini_cli.core.config import settings
from gemini_cli.core.output import ASPECT_RATIOS, console, print_models


@click.command()
def models() -> None:
    """List available Gemini models."""
    print_models()


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Gemini CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)


@click.command("aspect-ratios")
def aspect_ratios() -> None:
    """List available video aspect ratios."""
    from rich.table import Table

    table = Table(title="Available Video Aspect Ratios")
    table.add_column("Aspect Ratio", style="bold cyan")

    for ratio in ASPECT_RATIOS:
        table.add_row(ratio)

    console.print(table)

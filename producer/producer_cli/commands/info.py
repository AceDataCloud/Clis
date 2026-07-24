"""Info and utility commands."""

import click

from producer_cli.core.config import settings
from producer_cli.core.output import AUDIO_ACTIONS, console, print_models


@click.command()
def models() -> None:
    """List available Producer models."""
    print_models()


@click.command()
def actions() -> None:
    """List available audio generation actions."""
    from rich.table import Table

    table = Table(title="Available Audio Generation Actions")
    table.add_column("Action", style="bold cyan")
    table.add_column("Description")

    action_descriptions = {
        "generate": "Generate a new music track from a prompt",
        "cover": "Create a cover version of an existing track",
        "extend": "Extend an existing audio track",
        "variation": "Generate a variation of an existing track",
        "swap_vocals": "Swap the vocals in an existing track",
        "swap_instrumentals": "Swap the instrumentals in an existing track",
        "replace_section": "Replace a section of an existing track",
        "stems": "Extract stems (vocals, instruments) from a track",
    }

    for action in AUDIO_ACTIONS:
        table.add_row(action, action_descriptions.get(action, ""))

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Producer CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Default Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

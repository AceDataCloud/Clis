"""Info and utility commands."""

import click

from qwen_image_cli.core.config import settings
from qwen_image_cli.core.output import PROMPT_EXTEND_MODES, console, print_models


@click.command()
def models() -> None:
    """List available QwenImage models."""
    print_models()


@click.command("prompt-extend-modes")
def prompt_extend_modes() -> None:
    """List available prompt extension modes.

    Examples:

      qwen-image prompt-extend-modes
    """
    from rich.table import Table

    table = Table(title="Available Prompt Extend Modes")
    table.add_column("Mode", style="bold cyan")
    table.add_column("Description")

    table.add_row("direct", "Apply direct prompt extension")
    table.add_row("agent", "Use agent-based prompt extension")

    console.print(table)
    console.print(f"\n[dim]Available modes: {', '.join(PROMPT_EXTEND_MODES)}[/dim]")


@click.command()
def config() -> None:
    """Show current configuration.

    Examples:

      qwen-image config
    """
    from rich.table import Table

    table = Table(title="QwenImage CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token", f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]"
    )
    table.add_row("Default Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

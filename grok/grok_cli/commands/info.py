"""Info and utility commands."""

import click

from grok_cli.core.config import settings
from grok_cli.core.output import console, print_chat_models, print_video_models


@click.command()
@click.option(
    "--type",
    "model_type",
    type=click.Choice(["chat", "video", "all"]),
    default="all",
    help="Type of models to list (chat/video/all).",
)
def models(model_type: str) -> None:
    """List available Grok models."""
    if model_type in ("chat", "all"):
        print_chat_models()
    if model_type in ("video", "all"):
        print_video_models()


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Grok CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

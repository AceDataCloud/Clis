"""Info and utility commands."""

import click

from fish_cli.core.config import settings
from fish_cli.core.output import DEFAULT_TTS_MODEL, FISH_AUDIO_FORMATS, console


@click.command()
def models() -> None:
    """List available Fish AI TTS models."""
    from rich.table import Table

    table = Table(title="Available Fish AI TTS Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    table.add_row("s2-pro", "High-quality TTS model (default)")
    table.add_row("s1", "Standard TTS model")

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_TTS_MODEL}[/dim]")


@click.command()
def formats() -> None:
    """List available audio output formats."""
    from rich.table import Table

    table = Table(title="Available Audio Formats")
    table.add_column("Format", style="bold cyan")
    table.add_column("Notes")

    notes = {
        "mp3": "Compressed, widely supported (default)",
        "wav": "Uncompressed, high quality",
        "pcm": "Raw PCM audio data",
        "opus": "Compressed, low-latency",
    }
    for fmt in FISH_AUDIO_FORMATS:
        table.add_row(fmt, notes.get(fmt, ""))

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Fish CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token", f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]"
    )
    table.add_row("Default TTS Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

"""Info and utility commands for DrawAI CLI."""

import click

from drawai_cli.core.output import console, print_templates


@click.command()
def templates() -> None:
    """List available headshot templates."""
    print_templates()


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    from drawai_cli.core.config import settings

    table = Table(title="Configuration", show_header=False)
    table.add_column("Key", style="bold")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}...{settings.api_token[-4:]}"
        if len(settings.api_token) > 12
        else ("(not set)" if not settings.api_token else settings.api_token),
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

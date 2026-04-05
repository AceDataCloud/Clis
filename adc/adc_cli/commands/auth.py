"""Auth commands for token management."""

import click

from adc_cli.core.config import save_token_to_config, settings
from adc_cli.core.output import console, print_success


@click.group()
def auth() -> None:
    """Manage API authentication.

    \b
    Examples:
      adc auth login
      adc auth status
    """


@auth.command()
@click.option("--token", prompt="API Token", hide_input=True, help="Your AceDataCloud API token.")
def login(token: str) -> None:
    """Save your API token for future use.

    Get your token at https://platform.acedata.cloud

    Examples:

      adc auth login
    """
    save_token_to_config(token)
    print_success("Token saved successfully!")
    console.print("[dim]Token stored in ~/.config/adc/config[/dim]")


@auth.command()
def status() -> None:
    """Check current authentication status."""
    from rich.table import Table

    table = Table(title="Auth Status")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not configured[/red]",
    )
    table.add_row(
        "Status",
        "[green]Configured[/green]" if settings.is_configured else "[red]Not configured[/red]",
    )

    console.print(table)

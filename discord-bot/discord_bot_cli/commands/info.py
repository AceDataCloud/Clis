"""Info and utility commands."""

import click

from discord_bot_cli.core.config import settings
from discord_bot_cli.core.exceptions import DiscordBotError
from discord_bot_cli.core.output import console, print_error, print_health, print_json


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="Discord Bot CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("Base URL", settings.base_url or "[red]Not set[/red]")
    table.add_row(
        "Token",
        f"{settings.token[:8]}..." if settings.token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)


@click.command()
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def health(ctx: click.Context, output_json: bool) -> None:
    """Check the service health status.

    This endpoint does not require authentication.

    \\b
    Examples:
      discord-bot health
      discord-bot health --json
    """
    from discord_bot_cli.core.client import get_client

    try:
        client = get_client(
            base_url=ctx.obj.get("base_url"),
            token=ctx.obj.get("token"),
        )
        result = client.health()
        if output_json:
            print_json(result)
        else:
            print_health(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e

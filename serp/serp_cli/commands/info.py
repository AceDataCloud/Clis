"""Info and utility commands."""

import click

from serp_cli.core.config import settings
from serp_cli.core.output import console, print_search_types


@click.command("search-types")
def search_types() -> None:
    """List available search types."""
    print_search_types()


@click.command("time-ranges")
def time_ranges() -> None:
    """List available time range filters."""
    from rich.table import Table

    table = Table(title="Time Range Filters")
    table.add_column("Code", style="bold cyan")
    table.add_column("Period")
    table.add_column("Description")

    table.add_row("qdr:h", "Past Hour", "Results from the last hour")
    table.add_row("qdr:d", "Past Day", "Results from the last 24 hours")
    table.add_row("qdr:w", "Past Week", "Results from the last 7 days")
    table.add_row("qdr:m", "Past Month", "Results from the last 30 days")
    table.add_row("(none)", "Any Time", "No time restriction (default)")

    console.print(table)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="SERP CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

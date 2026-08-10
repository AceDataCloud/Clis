"""Output formatting helpers."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_result(data: dict[str, Any], title: str = "Result") -> None:
    """Print an API result in a compact rich format."""
    lines: list[str] = []
    for key in ("task_id", "trace_id", "id", "state", "url", "image_url", "video_url"):
        value = data.get(key)
        if value:
            lines.append(f"[bold]{key.replace('_', ' ').title()}:[/bold] {value}")
    if not lines:
        lines.append(json.dumps(data, indent=2, ensure_ascii=False))
    console.print(Panel("\n".join(lines), title=f"[bold green]{title}[/bold green]"))


def print_config(title: str, settings: Any) -> None:
    """Print current CLI configuration."""
    table = Table(title=title)
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")
    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")
    console.print(table)

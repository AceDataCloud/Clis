"""Rich terminal output formatting for Localization CLI."""

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


def print_translation_result(data: dict[str, Any]) -> None:
    """Print localization translation result."""
    if not data:
        console.print("[yellow]No result returned.[/yellow]")
        return

    table = Table(title="Localization Translation Result", show_header=False, box=None)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    for field in ("locale", "model"):
        value = data.get(field)
        if value:
            table.add_row(field.title(), str(value))

    translated = data.get("data")
    if translated is not None:
        table.add_row("Data", json.dumps(translated, indent=2, ensure_ascii=False))

    if table.row_count:
        console.print(table)
    else:
        console.print(
            Panel(
                json.dumps(data, indent=2, ensure_ascii=False),
                title="[bold green]Translation Result[/bold green]",
                border_style="green",
            )
        )

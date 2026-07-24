"""Rich terminal output formatting for Image2Text CLI."""

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


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_recognition_result(data: dict[str, Any]) -> None:
    """Print image2text recognition result."""
    task_id = data.get("task_id")
    text = data.get("text") or data.get("data", {})

    if task_id and not text:
        console.print(
            Panel(
                f"[bold]Task ID:[/bold] {task_id}",
                title="[bold green]Recognition Task Submitted[/bold green]",
                border_style="green",
            )
        )
        console.print("[dim]Poll with the task_id to retrieve the result.[/dim]")
        return

    if not text and not data:
        console.print("[yellow]No result returned.[/yellow]")
        return

    if isinstance(text, str) and text:
        table = Table(
            title="Image2Text Recognition Result", show_header=False, box=None, padding=(0, 2)
        )
        table.add_column("Field", style="bold cyan", width=12)
        table.add_column("Value")
        table.add_row("Text", text)
        console.print(table)
    else:
        console.print(
            Panel(
                json.dumps(data, indent=2, ensure_ascii=False),
                title="[bold green]Recognition Result[/bold green]",
                border_style="green",
            )
        )

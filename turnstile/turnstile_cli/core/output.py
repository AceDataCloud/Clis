"""Rich terminal output formatting for Turnstile CLI."""

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


def print_token_result(data: dict[str, Any]) -> None:
    """Print Turnstile token result."""
    token = data.get("token")
    task_id = data.get("task_id")

    if task_id and not token:
        # Async response
        content = f"[bold]Task ID:[/bold] {task_id}"
        console.print(
            Panel(
                content,
                title="[bold green]Token Task Submitted[/bold green]",
                border_style="green",
            )
        )
        console.print("[dim]Poll POST /captcha/tasks with the task_id to retrieve the token.[/dim]")
    elif token:
        table = Table(
            title="Turnstile Token Result", show_header=False, box=None, padding=(0, 2)
        )
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        table.add_row("Token", token)
        elapsed = data.get("elapsed")
        if elapsed is not None:
            table.add_row("Elapsed", f"{elapsed}s")
        console.print(table)
    else:
        console.print("[yellow]No token available yet.[/yellow]")

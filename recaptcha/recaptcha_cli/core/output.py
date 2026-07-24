"""Rich terminal output formatting for reCAPTCHA CLI."""

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
    """Print reCAPTCHA recognition result."""
    task_id = data.get("task_id")
    solution = data.get("solution", {})

    if task_id and not solution:
        console.print(
            Panel(
                f"[bold]Task ID:[/bold] {task_id}",
                title="[bold green]Recognition Task Submitted[/bold green]",
                border_style="green",
            )
        )
        console.print("[dim]Poll with the task_id to retrieve the result.[/dim]")
        return

    if not solution and not data:
        console.print("[yellow]No solution returned.[/yellow]")
        return

    if isinstance(solution, dict) and solution:
        table = Table(
            title="reCAPTCHA Recognition Result", show_header=False, box=None, padding=(0, 2)
        )
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key, value in solution.items():
            table.add_row(key.replace("_", " ").title(), str(value))
        console.print(table)
    else:
        console.print(
            Panel(
                json.dumps(data, indent=2, ensure_ascii=False),
                title="[bold green]Recognition Result[/bold green]",
                border_style="green",
            )
        )


def print_token_result(data: dict[str, Any]) -> None:
    """Print reCAPTCHA token result."""
    token = data.get("token")
    task_id = data.get("task_id")

    if task_id and not token:
        console.print(
            Panel(
                f"[bold]Task ID:[/bold] {task_id}",
                title="[bold green]Token Task Submitted[/bold green]",
                border_style="green",
            )
        )
        console.print("[dim]Poll with the task_id to retrieve the token.[/dim]")
    elif token:
        table = Table(title="reCAPTCHA Token Result", show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=12)
        table.add_column("Value")
        table.add_row("Token", token)
        user_agent = data.get("user_agent")
        if user_agent:
            table.add_row("User Agent", user_agent)
        console.print(table)
    else:
        console.print("[yellow]No token available yet.[/yellow]")

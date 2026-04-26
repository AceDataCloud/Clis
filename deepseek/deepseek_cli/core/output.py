"""Rich terminal output formatting for DeepSeek CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

MODELS = [
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v3.2-exp",
]

DEFAULT_MODEL = "deepseek-v3"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_chat_result(data: dict[str, Any]) -> None:
    """Print a chat completion result."""
    choices = data.get("choices", [])
    if choices:
        for i, choice in enumerate(choices, 1):
            message = choice.get("message", {})
            content = message.get("content", "")
            role = message.get("role", "assistant")
            finish_reason = choice.get("finish_reason", "")
            title = f"[bold green]Response #{i}[/bold green]" if len(choices) > 1 else "[bold green]Response[/bold green]"
            console.print(
                Panel(
                    content or "[dim](empty)[/dim]",
                    title=title,
                    subtitle=f"[dim]{role} · {finish_reason}[/dim]" if finish_reason else f"[dim]{role}[/dim]",
                    border_style="green",
                )
            )
    else:
        task_id = data.get("task_id", "")
        if task_id:
            console.print(
                Panel(
                    f"[bold]Task ID:[/bold] {task_id}",
                    title="[bold yellow]Queued[/bold yellow]",
                    border_style="yellow",
                )
            )
        else:
            console.print("[yellow]No response content available.[/yellow]")

    usage = data.get("usage", {})
    if usage:
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="dim")
        table.add_column("Value", style="dim")
        if usage.get("prompt_tokens"):
            table.add_row("Prompt tokens", str(usage["prompt_tokens"]))
        if usage.get("completion_tokens"):
            table.add_row("Completion tokens", str(usage["completion_tokens"]))
        if usage.get("total_tokens"):
            table.add_row("Total tokens", str(usage["total_tokens"]))
        console.print(table)


def print_models() -> None:
    """Print available models."""
    table = Table(title="Available DeepSeek Models")
    table.add_column("Model", style="bold cyan")
    for model in MODELS:
        table.add_row(model)
    console.print(table)

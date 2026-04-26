"""Rich terminal output formatting for Claude CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

MODELS = [
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-7-sonnet-20250219",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-haiku-4-5-20251001",
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-opus-4-5-20251101",
    "claude-opus-4-6",
    "claude-opus-4-7",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-6",
]

DEFAULT_MODEL = "claude-sonnet-4-20250514"


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
            title = (
                f"[bold green]Response #{i}[/bold green]"
                if len(choices) > 1
                else "[bold green]Response[/bold green]"
            )
            console.print(
                Panel(
                    content or "[dim](empty)[/dim]",
                    title=title,
                    subtitle=f"[dim]{role} · {finish_reason}[/dim]" if finish_reason else f"[dim]{role}[/dim]",
                    border_style="green",
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


def print_messages_result(data: dict[str, Any]) -> None:
    """Print a native Claude Messages API result."""
    content_list = data.get("content", [])
    if content_list:
        text_parts = [item.get("text", "") for item in content_list if item.get("type") == "text"]
        text = "\n".join(text_parts)
        role = data.get("role", "assistant")
        stop_reason = data.get("stop_reason", "")
        console.print(
            Panel(
                text or "[dim](empty)[/dim]",
                title="[bold green]Response[/bold green]",
                subtitle=f"[dim]{role} · {stop_reason}[/dim]" if stop_reason else f"[dim]{role}[/dim]",
                border_style="green",
            )
        )
    else:
        console.print("[yellow]No response content available.[/yellow]")

    usage = data.get("usage", {})
    if usage:
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="dim")
        table.add_column("Value", style="dim")
        if usage.get("input_tokens"):
            table.add_row("Input tokens", str(usage["input_tokens"]))
        if usage.get("output_tokens"):
            table.add_row("Output tokens", str(usage["output_tokens"]))
        console.print(table)


def print_token_count_result(data: dict[str, Any]) -> None:
    """Print a token count result."""
    input_tokens = data.get("input_tokens", 0)
    console.print(
        Panel(
            f"[bold]Input tokens:[/bold] {input_tokens}",
            title="[bold green]Token Count[/bold green]",
            border_style="green",
        )
    )


def print_models() -> None:
    """Print available Claude models."""
    table = Table(title="Available Claude Models")
    table.add_column("Model", style="bold cyan")
    for model in MODELS:
        table.add_row(model)
    console.print(table)

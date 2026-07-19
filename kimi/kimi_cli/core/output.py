"""Rich terminal output formatting for Kimi CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available Kimi models from OpenAPI spec
KIMI_MODELS = [
    "kimi-k3",
    "kimi-k2.6",
    "kimi-k2-thinking-turbo",
    "kimi-k2.5",
    "kimi-k2-thinking",
    "kimi-k2-instruct-0905",
    "kimi-k2-0905-preview",
    "kimi-k2-turbo-preview",
    "kimi-k2-0711-preview",
]

DEFAULT_MODEL = "kimi-k2.6"

# Available reasoning efforts
REASONING_EFFORTS = ["standard", "high", "max"]

# Available service tiers
SERVICE_TIERS = ["auto", "default", "flex", "scale", "priority"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


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
                    subtitle=(
                        f"[dim]{role} \u00b7 {finish_reason}[/dim]"
                        if finish_reason
                        else f"[dim]{role}[/dim]"
                    ),
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


def print_models() -> None:
    """Print available Kimi models."""
    table = Table(title="Available Kimi Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    model_notes = {
        "kimi-k3": "Kimi K3 (latest)",
        "kimi-k2.6": "Kimi K2.6 (default)",
        "kimi-k2-thinking-turbo": "Kimi K2 Thinking Turbo",
        "kimi-k2.5": "Kimi K2.5",
        "kimi-k2-thinking": "Kimi K2 Thinking",
        "kimi-k2-instruct-0905": "Kimi K2 Instruct 0905",
        "kimi-k2-0905-preview": "Kimi K2 0905 Preview",
        "kimi-k2-turbo-preview": "Kimi K2 Turbo Preview",
        "kimi-k2-0711-preview": "Kimi K2 0711 Preview",
    }

    for model in KIMI_MODELS:
        table.add_row(model, model_notes.get(model, ""))

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

"""Rich terminal output formatting for Fish CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
FISH_MODELS = [
    "fish-tts",
]

DEFAULT_MODEL = "fish-tts"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_audio_result(data: dict[str, Any]) -> None:
    """Print audio generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    items = data.get("data", [])

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Audio Result[/bold green]",
            border_style="green",
        )
    )

    if not items:
        console.print("[yellow]No data available yet. Use 'task' to check status.[/yellow]")
        return

    if isinstance(items, list):
        for i, item in enumerate(items, 1):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            table.add_row("Audio", f"#{i}")
            if item.get("audio_url"):
                table.add_row("URL", item["audio_url"])
            if item.get("state"):
                table.add_row("State", item["state"])
            if item.get("model"):
                table.add_row("Model", item["model"])
            if item.get("created_at"):
                table.add_row("Created", item["created_at"])
            console.print(table)
            console.print()
    elif isinstance(items, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        if items.get("audio_url"):
            table.add_row("URL", items["audio_url"])
        if items.get("state"):
            table.add_row("State", items["state"])
        if items.get("model"):
            table.add_row("Model", items["model"])
        if items.get("created_at"):
            table.add_row("Created", items["created_at"])
        console.print(table)


def print_voice_result(data: dict[str, Any]) -> None:
    """Print voice cloning result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    items = data.get("data", {})

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Voice Result[/bold green]",
            border_style="green",
        )
    )

    if not items:
        console.print("[yellow]No data available yet. Use 'task' to check status.[/yellow]")
        return

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")

    if isinstance(items, dict):
        for key in ["voice_id", "title", "state", "created_at"]:
            if items.get(key):
                table.add_row(key.replace("_", " ").title(), str(items[key]))
    elif isinstance(items, list):
        for item in items:
            for key in ["voice_id", "title", "state", "created_at"]:
                if item.get(key):
                    table.add_row(key.replace("_", " ").title(), str(item[key]))
            console.print(table)
            console.print()
            return

    console.print(table)


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    tasks = data.get("data", [])

    if isinstance(tasks, list):
        for task_data in tasks:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")

            for key in ["id", "status", "state", "audio_url", "model", "created_at"]:
                if task_data.get(key):
                    table.add_row(key.replace("_", " ").title(), str(task_data[key]))

            console.print(table)
            console.print()
    elif isinstance(tasks, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")

        for key in ["id", "status", "state", "audio_url", "model", "created_at"]:
            if tasks.get(key):
                table.add_row(key.replace("_", " ").title(), str(tasks[key]))

        console.print(table)


def print_models() -> None:
    """Print available Fish models."""
    table = Table(title="Available Fish Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    model_notes = {
        "fish-tts": "Default model for text-to-speech with voice cloning",
    }

    for model in FISH_MODELS:
        table.add_row(model, model_notes.get(model, ""))

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

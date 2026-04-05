"""Rich terminal output formatting for Luma CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
LUMA_MODELS = [
    ("luma", "Standard", "Standard quality video generation (default)"),
]

# Available aspect ratios
ASPECT_RATIOS = [
    "16:9",
    "9:16",
    "1:1",
    "4:3",
    "3:4",
    "21:9",
    "9:21",
]

DEFAULT_ASPECT_RATIO = "16:9"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_models() -> None:
    """Print available Luma models."""
    table = Table(title="Available Luma Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Version")
    table.add_column("Notes")

    for model, version, notes in LUMA_MODELS:
        table.add_row(model, version, notes)

    console.print(table)


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_video_result(data: dict[str, Any]) -> None:
    """Print video generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    items = data.get("data", [])

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Video Result[/bold green]",
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
            table.add_row("Video", f"#{i}")
            if item.get("video_url"):
                table.add_row("URL", item["video_url"])
            if item.get("state"):
                table.add_row("State", item["state"])
            if item.get("model_name"):
                table.add_row("Model", item["model_name"])
            if item.get("created_at"):
                table.add_row("Created", item["created_at"])
            console.print(table)
            console.print()


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    tasks = data.get("data", [])

    if isinstance(tasks, list):
        for task_data in tasks:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")

            for key in ["id", "status", "state", "video_url", "model_name", "created_at"]:
                if task_data.get(key):
                    table.add_row(key.replace("_", " ").title(), str(task_data[key]))

            console.print(table)
            console.print()
    elif isinstance(tasks, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")

        for key in ["id", "status", "state", "video_url", "model_name", "created_at"]:
            if tasks.get(key):
                table.add_row(key.replace("_", " ").title(), str(tasks[key]))

        console.print(table)



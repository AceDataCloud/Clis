"""Rich terminal output formatting for Hailuo CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
HAILUO_MODELS = [
    "minimax-t2v",
    "minimax-i2v",
    "minimax-i2v-director",
]

DEFAULT_MODEL = "minimax-t2v"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_video_result(data: dict[str, Any]) -> None:
    """Print video generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Video Result[/bold green]",
            border_style="green",
        )
    )

    video_url = data.get("video_url")
    if video_url:
        console.print(f"[bold]Video URL:[/bold] {video_url}")
    elif not data.get("task_id"):
        console.print("[yellow]No video available yet. Use 'task' to check status.[/yellow]")
    else:
        console.print("[yellow]Video is being generated. Use 'task' to check status.[/yellow]")


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    # Handle single task response
    if isinstance(data.get("data"), dict):
        task_data = data["data"]
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key in ["id", "status", "state", "video_url", "model", "created_at"]:
            if task_data.get(key):
                table.add_row(key.replace("_", " ").title(), str(task_data[key]))
        console.print(table)
        return

    # Handle batch response
    items = data.get("data", [])
    if isinstance(items, list) and items:
        for item in items:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            for key in ["id", "status", "state", "video_url", "model", "created_at"]:
                if item.get(key):
                    table.add_row(key.replace("_", " ").title(), str(item[key]))
            console.print(table)
            console.print()
        return

    # Handle direct top-level task fields
    if data.get("task_id") or data.get("video_url"):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key in ["task_id", "video_url", "model", "status", "state"]:
            val = data.get(key)
            if val:
                table.add_row(key.replace("_", " ").title(), str(val))
        console.print(table)
        return

    console.print("[yellow]No data available.[/yellow]")


def print_models() -> None:
    """Print available Hailuo models."""
    table = Table(title="Available Hailuo Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Type")
    table.add_column("Notes")

    table.add_row("minimax-t2v", "Text-to-Video", "Generate video from text prompt (default)")
    table.add_row("minimax-i2v", "Image-to-Video", "Generate video from image + text")
    table.add_row(
        "minimax-i2v-director", "Image-to-Video", "Cinematic director mode with image reference"
    )

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

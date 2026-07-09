"""Rich terminal output formatting for HappyHorse CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
HAPPYHORSE_MODELS = [
    "happyhorse-1.0-t2v",
    "happyhorse-1.1-t2v",
    "happyhorse-1.0-i2v",
    "happyhorse-1.1-i2v",
    "happyhorse-1.0-r2v",
    "happyhorse-1.1-r2v",
    "happyhorse-1.0-video-edit",
]

DEFAULT_MODEL = "happyhorse-1.1-t2v"


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

    # Check for video URLs in data array
    items = data.get("data", [])
    if isinstance(items, list) and items:
        for item in items:
            video_url = item.get("video_url")
            if video_url:
                console.print(f"[bold]Video URL:[/bold] {video_url}")
                return
    elif isinstance(items, dict):
        video_url = items.get("video_url")
        if video_url:
            console.print(f"[bold]Video URL:[/bold] {video_url}")
            return

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
    """Print available HappyHorse models."""
    table = Table(title="Available HappyHorse Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Type")
    table.add_column("Notes")

    table.add_row("happyhorse-1.0-t2v", "Text-to-Video", "Generate video from text prompt")
    table.add_row(
        "happyhorse-1.1-t2v", "Text-to-Video", "Generate video from text prompt (default)"
    )
    table.add_row("happyhorse-1.0-i2v", "Image-to-Video", "Generate video from image")
    table.add_row("happyhorse-1.1-i2v", "Image-to-Video", "Generate video from image")
    table.add_row("happyhorse-1.0-r2v", "Reference-to-Video", "Generate video from reference")
    table.add_row("happyhorse-1.1-r2v", "Reference-to-Video", "Generate video from reference")
    table.add_row(
        "happyhorse-1.0-video-edit", "Video Edit", "Edit video with text instructions"
    )

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

"""Rich terminal output formatting for Hailuo CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
HAILUO_MODELS = [
    "minimax-i2v",
    "minimax-t2v",
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

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}",
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

    def print_task(task_data: dict[str, Any]) -> None:
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key in ["id", "status", "model", "resolution", "duration", "ratio", "created_at"]:
            if task_data.get(key):
                table.add_row(key.replace("_", " ").title(), str(task_data[key]))
        content = task_data.get("content")
        if isinstance(content, dict) and content.get("url"):
            table.add_row("Video Url", str(content["url"]))
        console.print(table)

    if isinstance(data.get("task"), dict):
        print_task(data["task"])
        return

    items = data.get("items", [])
    if isinstance(items, list) and items:
        for item in items:
            if isinstance(item, dict):
                print_task(item)
            console.print()
        return

    if data.get("id") and "deleted" in data:
        print_success(f"Task {data['id']} deleted.")
        return

    console.print("[yellow]No data available.[/yellow]")


def print_models() -> None:
    """Print available Hailuo models."""
    table = Table(title="Available Hailuo Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Type")
    table.add_column("Notes")

    table.add_row("minimax-t2v", "Text to Video", "Generate a video from a prompt")
    table.add_row("minimax-i2v", "Image to Video", "Generate a video from a first-frame image")
    table.add_row("minimax-i2v-director", "Image to Video", "Director-controlled image animation")

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

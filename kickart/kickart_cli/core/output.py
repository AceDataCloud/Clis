"""Rich terminal output formatting for Kickart CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Video generation modes
VIDEO_MODES = ["fast", "pro"]
VIDEO_TYPES = ["intro", "main"]
VIDEO_DURATIONS = [15, 30, 45, 60]
ASPECT_RATIOS = ["9:16", "16:9", "3:4", "4:3", "1:1"]
LANGUAGES = ["zh", "en", "en-us", "pt-br", "ja", "es-mx", "id", "ms", "tl"]

# Viral video modes
VIRAL_MODES = ["pro", "advanced"]
SIMILARITY_LEVELS = ["high", "medium"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


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
            title="[bold green]Video Generation Result[/bold green]",
            border_style="green",
        )
    )

    items = data.get("data", [])
    if not items:
        console.print("[yellow]No data available yet. Poll with the task_id to check status.[/yellow]")
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
            console.print(table)
            console.print()
    elif isinstance(items, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        if items.get("task_id"):
            table.add_row("Task ID", items["task_id"])
        if items.get("video_url"):
            table.add_row("URL", items["video_url"])
        if items.get("state"):
            table.add_row("State", items["state"])
        console.print(table)

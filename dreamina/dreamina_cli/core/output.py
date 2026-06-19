"""Rich terminal output formatting for Dreamina CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available Dreamina models
DREAMINA_MODELS = [
    "omnihuman-1.5",
]

DEFAULT_MODEL = "omnihuman-1.5"


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

    item = data.get("data", {})
    if not item:
        console.print("[yellow]No data available yet. Use 'task' to check status.[/yellow]")
        return

    if isinstance(item, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        if item.get("task_id"):
            table.add_row("Task ID", item["task_id"])
        if item.get("status"):
            table.add_row("Status", item["status"])
        if item.get("video_url"):
            table.add_row("Video URL", item["video_url"])
        if item.get("image_url"):
            table.add_row("Image URL", item["image_url"])
        if item.get("audio_url"):
            table.add_row("Audio URL", item["audio_url"])
        console.print(table)


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    task_id = data.get("id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Task Result[/bold green]",
            border_style="green",
        )
    )

    response = data.get("response", {})
    if response:
        inner = response.get("data", {})
        if isinstance(inner, dict):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            if inner.get("task_id"):
                table.add_row("Task ID", inner["task_id"])
            if inner.get("status"):
                table.add_row("Status", inner["status"])
            if inner.get("video_url"):
                table.add_row("Video URL", inner["video_url"])
            if inner.get("image_url"):
                table.add_row("Image URL", inner["image_url"])
            if inner.get("audio_url"):
                table.add_row("Audio URL", inner["audio_url"])
            console.print(table)


def print_models() -> None:
    """Print available Dreamina models."""
    table = Table(title="Available Dreamina Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    table.add_row("omnihuman-1.5", "OmniHuman (default)")

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

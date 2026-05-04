"""Rich terminal output formatting for Veo CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
VEO_MODELS = [
    "veo3",
    "veo3-fast",
    "veo31",
    "veo31-fast",
    "veo31-fast-ingredients",
    "veo2",
    "veo2-fast",
]

DEFAULT_MODEL = "veo3"

# Available aspect ratios
ASPECT_RATIOS = [
    "16:9",
    "9:16",
    "3:4",
    "4:3",
    "1:1",
]

# Models supported by the extend endpoint
EXTEND_MODELS = [
    "veo31-fast",
    "veo31",
]

# Available resolutions
RESOLUTIONS = [
    "4k",
    "1080p",
    "gif",
]

# Camera motion types for reshoot
MOTION_TYPES = [
    "STATIONARY",
    "STATIONARY_PAN_LEFT",
    "STATIONARY_PAN_RIGHT",
    "STATIONARY_TILT_UP",
    "STATIONARY_TILT_DOWN",
    "STATIONARY_DOLLY_ZOOM_IN",
    "STATIONARY_DOLLY_ZOOM_OUT",
    "UP",
    "DOWN",
    "LEFT_TO_RIGHT",
    "RIGHT_TO_LEFT",
    "FORWARD",
    "BACKWARD",
    "DOLLY_IN_ZOOM_OUT",
    "DOLLY_OUT_ZOOM_IN",
]

DEFAULT_ASPECT_RATIO = "16:9"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


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


def print_models() -> None:
    """Print available Veo models."""
    table = Table(title="Available Veo Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Version", style="bold")
    table.add_column("Notes")

    table.add_row(
        "veo3",
        "V3",
        "Latest model, best quality (default)",
    )
    table.add_row(
        "veo3-fast",
        "V3 Fast",
        "Fast generation",
    )
    table.add_row(
        "veo31",
        "V3.1",
        "Next generation model",
    )
    table.add_row(
        "veo31-fast",
        "V3.1 Fast",
        "Fast next-gen model",
    )
    table.add_row(
        "veo31-fast-ingredients",
        "V3.1 Fast Ingredient",
        "Ingredient-based fast next-gen model",
    )
    table.add_row(
        "veo2",
        "V2",
        "Previous generation, stable",
    )
    table.add_row(
        "veo2-fast",
        "V2 Fast",
        "Fast previous-gen model",
    )

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

"""Rich terminal output formatting for Seedream CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
SEEDREAM_MODELS = [
    "doubao-seedream-5-0-260128",
    "doubao-seedream-4-5-251128",
    "doubao-seedream-4-0-250828",
    "doubao-seedream-3-0-t2i-250415",
    "doubao-seededit-3-0-i2i-250628",
]

DEFAULT_MODEL = "doubao-seedream-5-0-260128"

# Available resolutions
RESOLUTIONS = [
    "1K",
    "2K",
    "3K",
    "4K",
    "adaptive",
]

DEFAULT_RESOLUTION = "1K"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_image_result(data: dict[str, Any]) -> None:
    """Print image generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    items = data.get("data", [])

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Image Result[/bold green]",
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
            table.add_row("Image", f"#{i}")
            if item.get("image_url"):
                table.add_row("URL", item["image_url"])
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

            for key in ["id", "status", "state", "image_url", "model_name", "created_at"]:
                if task_data.get(key):
                    table.add_row(key.replace("_", " ").title(), str(task_data[key]))

            console.print(table)
            console.print()
    elif isinstance(tasks, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")

        for key in ["id", "status", "state", "image_url", "model_name", "created_at"]:
            if tasks.get(key):
                table.add_row(key.replace("_", " ").title(), str(tasks[key]))

        console.print(table)


def print_models() -> None:
    """Print available Seedream models."""
    table = Table(title="Available Seedream Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Version", style="bold")
    table.add_column("Notes")

    table.add_row(
        "doubao-seedream-5-0-260128",
        "V5.0",
        "Latest model (default)",
    )
    table.add_row(
        "doubao-seedream-4-5-251128",
        "V4.5",
        "Flagship model, best quality",
    )
    table.add_row(
        "doubao-seedream-4-0-250828",
        "V4.0",
        "Standard quality",
    )
    table.add_row(
        "doubao-seedream-3-0-t2i-250415",
        "V3.0 T2I",
        "Text-to-image generation",
    )
    table.add_row(
        "doubao-seededit-3-0-i2i-250628",
        "V3.0 I2I",
        "Image-to-image editing",
    )

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

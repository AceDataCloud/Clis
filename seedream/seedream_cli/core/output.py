"""Rich terminal output formatting for Seedream CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
SEEDREAM_MODELS = [
    "doubao-seedream-5-0-pro-260628",
    "doubao-seedream-5-0-260128",
    "doubao-seedream-5-0-lite-260128",
    "doubao-seedream-4-5-251128",
    "doubao-seedream-4-0-250828",
]

DEFAULT_MODEL = "doubao-seedream-5-0-260128"

# Available resolutions
RESOLUTIONS = [
    "1K",
    "1.5K",
    "2K",
    "3K",
    "4K",
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
            if item.get("size"):
                table.add_row("Size", str(item["size"]))
            if item.get("output_format"):
                table.add_row("Format", str(item["output_format"]))
            if item.get("z_index") is not None:
                table.add_row("Z-index", str(item["z_index"]))
            if item.get("name"):
                table.add_row("Layer", str(item["name"]))
            if item.get("description"):
                table.add_row("Description", str(item["description"]))
            if item.get("bounding_box"):
                table.add_row("Bounding box", json.dumps(item["bounding_box"], ensure_ascii=False))
            if item.get("error"):
                table.add_row("Error", json.dumps(item["error"], ensure_ascii=False))
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
    table.add_column("Model", style="bold cyan", no_wrap=True)
    table.add_column("Version", style="bold")
    table.add_column("Notes")

    table.add_row(
        "doubao-seedream-5-0-pro-260628",
        "V5.0 Pro",
        "Single image, transparent background, layer decomposition",
    )
    table.add_row(
        "doubao-seedream-5-0-260128",
        "doubao-seedream-5-0-lite-260128",
        "V5.0 Lite",
        "Sequential images, streaming, web search (default)",
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
    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

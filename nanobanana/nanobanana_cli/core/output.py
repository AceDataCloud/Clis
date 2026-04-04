"""Rich terminal output formatting for NanoBanana CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
NANOBANANA_MODELS = [
    "nano-banana",
    "nano-banana-2",
    "nano-banana-pro",
]

DEFAULT_MODEL = "nano-banana"

# Available aspect ratios
ASPECT_RATIOS = [
    "1:1",
    "3:2",
    "2:3",
    "16:9",
    "9:16",
    "4:3",
    "3:4",
]

DEFAULT_ASPECT_RATIO = "1:1"

# Available resolutions (nano-banana-pro only)
RESOLUTIONS = [
    "1K",
    "2K",
    "4K",
]


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
    """Print image generation/edit result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    images = data.get("data", [])

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Image Result[/bold green]",
            border_style="green",
        )
    )

    if not images:
        console.print("[yellow]No image data available yet. Use 'task' to check status.[/yellow]")
        return

    if isinstance(images, list):
        for i, img in enumerate(images, 1):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            table.add_row("Image", f"#{i}")
            if img.get("image_url"):
                table.add_row("URL", img["image_url"])
            if img.get("state"):
                table.add_row("State", img["state"])
            if img.get("model_name"):
                table.add_row("Model", img["model_name"])
            if img.get("created_at"):
                table.add_row("Created", img["created_at"])
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
    """Print available NanoBanana models."""
    table = Table(title="Available NanoBanana Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Description")
    table.add_column("Features")

    table.add_row(
        "nano-banana",
        "Fast generation (Gemini 2.5 Flash)",
        "Quick, good quality",
    )
    table.add_row(
        "nano-banana-2",
        "Improved generation",
        "Better quality, balanced speed",
    )
    table.add_row(
        "nano-banana-pro",
        "Best quality (Gemini 3 Pro)",
        "Highest quality, resolution control (1K/2K/4K)",
    )

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

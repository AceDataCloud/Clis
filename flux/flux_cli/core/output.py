"""Rich terminal output formatting for Flux CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
FLUX_MODELS = [
    "flux-dev",
    "flux-pro",
    "flux-pro-1.1",
    "flux-pro-1.1-ultra",
    "flux-kontext-pro",
    "flux-kontext-max",
]
DEFAULT_MODEL = "flux-dev"

# Available aspect ratios (for ultra/kontext models)
ASPECT_RATIOS = [
    "1:1",
    "16:9",
    "21:9",
    "3:2",
    "2:3",
    "4:5",
    "5:4",
    "3:4",
    "4:3",
    "9:16",
    "9:21",
]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_image_result(data: dict[str, Any]) -> None:
    """Print image generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Image Result[/bold green]",
            border_style="green",
        )
    )

    items = data.get("data", [])
    if isinstance(items, list) and items:
        for i, item in enumerate(items, 1):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            table.add_row("Image", f"#{i}")
            if item.get("image_url"):
                table.add_row("URL", item["image_url"])
            if item.get("model"):
                table.add_row("Model", item["model"])
            if item.get("created_at"):
                table.add_row("Created", item["created_at"])
            console.print(table)
            console.print()
    else:
        console.print("[yellow]No image available yet. Use 'task' to check status.[/yellow]")


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    # Handle data array response
    items = data.get("data", [])
    if isinstance(items, list) and items:
        for item in items:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            for key in ["image_url", "model", "created_at"]:
                if item.get(key):
                    table.add_row(key.replace("_", " ").title(), str(item[key]))
            console.print(table)
            console.print()
        return

    # Handle batch response
    batch_items = data.get("items", [])
    if batch_items:
        for item in batch_items:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            for key in ["id", "type", "created_at"]:
                if item.get(key):
                    table.add_row(key.replace("_", " ").title(), str(item[key]))
            resp = item.get("response", {})
            resp_data = resp.get("data", [])
            if isinstance(resp_data, list):
                for img in resp_data:
                    if img.get("image_url"):
                        table.add_row("Image URL", img["image_url"])
            console.print(table)
            console.print()
        return

    console.print("[yellow]No data available.[/yellow]")


def print_models() -> None:
    """Print available Flux models."""
    table = Table(title="Available Flux Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Type")
    table.add_column("Size Input")
    table.add_column("Notes")

    table.add_row("flux-dev", "Dev", "Pixels", "Fast, good balance (default)")
    table.add_row("flux-pro", "Pro", "Pixels", "Higher quality")
    table.add_row("flux-pro-1.1", "Pro", "Pixels", "Better prompt following")
    table.add_row("flux-pro-1.1-ultra", "Ultra", "Aspect ratio", "Highest quality")
    table.add_row("flux-kontext-pro", "Kontext", "Aspect ratio", "Best for editing/style transfer")
    table.add_row("flux-kontext-max", "Kontext", "Aspect ratio", "Max context for complex edits")

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

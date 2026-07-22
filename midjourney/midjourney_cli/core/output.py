"""Rich terminal output formatting for Midjourney CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available modes for imagine/edits
IMAGINE_MODES = ["fast", "relax", "turbo"]
DEFAULT_IMAGINE_MODE = "fast"

# Available modes for videos
VIDEO_MODES = ["fast", "turbo"]

# Available video actions
VIDEO_ACTIONS = ["generate", "extend"]

# Available video resolutions
VIDEO_RESOLUTIONS = ["480p", "720p"]

# Available task actions
TASK_ACTIONS = ["retrieve", "retrieve_batch"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_result(data: dict[str, Any], title: str = "Result") -> None:
    """Print an API result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    items = data.get("data", [])

    info_lines = []
    if task_id != "N/A":
        info_lines.append(f"[bold]Task ID:[/bold] {task_id}")
    if trace_id != "N/A":
        info_lines.append(f"[bold]Trace ID:[/bold] {trace_id}")

    if info_lines:
        console.print(
            Panel(
                "\n".join(info_lines),
                title=f"[bold green]{title}[/bold green]",
                border_style="green",
            )
        )

    if not items:
        console.print("[yellow]No data available yet. Use 'task' to check status.[/yellow]")
        return

    _print_data_items(items)


def _print_data_items(items: Any) -> None:
    """Print data items from an API response."""
    if isinstance(items, list):
        for i, item in enumerate(items, 1):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            table.add_row("Item", f"#{i}")
            for key in [
                "id",
                "state",
                "status",
                "image_url",
                "image_urls",
                "video_url",
                "seed",
                "descriptions",
                "shortened_prompts",
                "translated_content",
                "model_name",
                "created_at",
            ]:
                val = item.get(key)
                if val is not None:
                    if isinstance(val, list):
                        val = ", ".join(str(v) for v in val)
                    table.add_row(key.replace("_", " ").title(), str(val))
            console.print(table)
            console.print()
    elif isinstance(items, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key in [
            "id",
            "state",
            "status",
            "image_url",
            "image_urls",
            "video_url",
            "seed",
            "descriptions",
            "prompts",
            "content",
            "model_name",
            "created_at",
        ]:
            val = items.get(key)
            if val is not None:
                if isinstance(val, list):
                    val = ", ".join(str(v) for v in val)
                table.add_row(key.replace("_", " ").title(), str(val))
        console.print(table)
    else:
        console.print(str(items))


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    tasks = data.get("data", [])
    _print_data_items(tasks)

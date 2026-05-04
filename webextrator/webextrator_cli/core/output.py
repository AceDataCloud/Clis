"""Rich terminal output formatting for WebExtrator CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Wait-until options
WAIT_UNTIL_OPTIONS = ["load", "domcontentloaded", "networkidle", "commit"]

# Block resource types
BLOCK_RESOURCE_TYPES = ["image", "font", "media", "stylesheet", "xhr", "fetch"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_extract_result(data: dict[str, Any]) -> None:
    """Print an extract result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    elapsed = data.get("elapsed", "N/A")
    result_data = data.get("data", {})

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n"
            f"[bold]Trace ID:[/bold] {trace_id}\n"
            f"[bold]Elapsed:[/bold] {elapsed}s",
            title="[bold green]Extract Result[/bold green]",
            border_style="green",
        )
    )

    if result_data and isinstance(result_data, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key in ["url", "contentType", "title", "description", "siteName"]:
            if result_data.get(key):
                table.add_row(key, str(result_data[key]))
        console.print(table)


def print_render_result(data: dict[str, Any]) -> None:
    """Print a render result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    elapsed = data.get("elapsed", "N/A")
    result_data = data.get("data", {})

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n"
            f"[bold]Trace ID:[/bold] {trace_id}\n"
            f"[bold]Elapsed:[/bold] {elapsed}s",
            title="[bold green]Render Result[/bold green]",
            border_style="green",
        )
    )

    if result_data and isinstance(result_data, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key in ["url", "finalUrl", "title", "status"]:
            if result_data.get(key) is not None:
                table.add_row(key, str(result_data[key]))
        html = result_data.get("html", "")
        if html:
            table.add_row("HTML length", f"{len(html)} chars")
        console.print(table)


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    items = data.get("items", None)
    if items is not None:
        # Batch result
        count = data.get("count", len(items))
        console.print(f"[bold]Tasks found:[/bold] {count}")
        for item in items:
            _print_single_task(item)
    else:
        _print_single_task(data)


def _print_single_task(task_data: dict[str, Any]) -> None:
    """Print a single task row."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")
    for key in ["id", "task_id", "trace_id", "type", "started_at", "finished_at", "elapsed"]:
        if task_data.get(key) is not None:
            table.add_row(key.replace("_", " ").title(), str(task_data[key]))
    console.print(table)
    console.print()

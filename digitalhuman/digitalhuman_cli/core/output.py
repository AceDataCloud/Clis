"""Rich terminal output formatting for Digital Human CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available engines
ENGINES = ["latentsync", "heygem"]
DEFAULT_ENGINE = "latentsync"

# Available resolutions
RESOLUTIONS = ["720p", "540p"]
DEFAULT_RESOLUTION = "720p"

# Available voice languages
VOICE_LANGUAGES = ["zh", "en"]
DEFAULT_VOICE_LANGUAGE = "zh"


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

    info_lines = [
        f"[bold]Task ID:[/bold] {task_id}",
        f"[bold]Trace ID:[/bold] {trace_id}",
    ]

    if data.get("state"):
        info_lines.append(f"[bold]State:[/bold] {data['state']}")
    if data.get("video_url"):
        info_lines.append(f"[bold]Video URL:[/bold] {data['video_url']}")
    if data.get("engine"):
        info_lines.append(f"[bold]Engine:[/bold] {data['engine']}")

    console.print(
        Panel(
            "\n".join(info_lines),
            title="[bold green]Digital Human Video Result[/bold green]",
            border_style="green",
        )
    )


def print_voice_result(data: dict[str, Any]) -> None:
    """Print voice cloning result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    info_lines = [
        f"[bold]Task ID:[/bold] {task_id}",
        f"[bold]Trace ID:[/bold] {trace_id}",
    ]

    if data.get("state"):
        info_lines.append(f"[bold]State:[/bold] {data['state']}")
    if data.get("voice_id"):
        info_lines.append(f"[bold]Voice ID:[/bold] {data['voice_id']}")

    console.print(
        Panel(
            "\n".join(info_lines),
            title="[bold green]Voice Clone Result[/bold green]",
            border_style="green",
        )
    )


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")

    for key in ["task_id", "state", "progress", "video_url", "voice_id", "engine"]:
        if data.get(key) is not None:
            table.add_row(key.replace("_", " ").title(), str(data[key]))

    console.print(table)


def print_engines() -> None:
    """Print available engines."""
    table = Table(title="Available Engines")
    table.add_column("Engine", style="bold cyan")
    table.add_column("Description")

    table.add_row("latentsync", "Quality engine, best lip-sync (default)")
    table.add_row("heygem", "Fast engine, lower latency")

    console.print(table)
    console.print(f"\n[dim]Default engine: {DEFAULT_ENGINE}[/dim]")

"""Rich terminal output formatting for Producer CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models
PRODUCER_MODELS = [
    "FUZZ-2.0 Pro",
    "FUZZ-2.0",
    "FUZZ-2.0 Raw",
    "FUZZ-1.1 Pro",
    "FUZZ-1.0 Pro",
    "FUZZ-1.0",
    "FUZZ-1.1",
    "FUZZ-0.8",
]

DEFAULT_MODEL = "FUZZ-2.0"

# Available actions for audio generation
AUDIO_ACTIONS = [
    "generate",
    "cover",
    "extend",
    "variation",
    "swap_vocals",
    "swap_instrumentals",
    "replace_section",
    "stems",
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


def print_audio_result(data: dict[str, Any]) -> None:
    """Print audio generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    items = data.get("data", [])

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Audio Result[/bold green]",
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
            table.add_row("Audio", f"#{i}")
            if item.get("title"):
                table.add_row("Title", item["title"])
            if item.get("audio_url"):
                table.add_row("Audio URL", item["audio_url"])
            if item.get("video_url"):
                table.add_row("Video URL", item["video_url"])
            if item.get("state"):
                table.add_row("State", item["state"])
            if item.get("model_name"):
                table.add_row("Model", item["model_name"])
            if item.get("duration"):
                table.add_row("Duration", f"{item['duration']}s")
            if item.get("created_at"):
                table.add_row("Created", item["created_at"])
            console.print(table)
            console.print()


def print_lyrics_result(data: dict[str, Any]) -> None:
    """Print lyrics generation result in a rich format."""
    lyrics_data = data.get("data", {})

    if isinstance(lyrics_data, dict):
        title = lyrics_data.get("title", "Generated Lyrics")
        text = lyrics_data.get("text", "")
        console.print(
            Panel(
                text or "[dim](no lyrics)[/dim]",
                title=f"[bold green]{title}[/bold green]",
                border_style="green",
            )
        )
    else:
        print_json(data)


def print_upload_result(data: dict[str, Any]) -> None:
    """Print audio upload result in a rich format."""
    upload_data = data.get("data", {})

    if isinstance(upload_data, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")

        if upload_data.get("audio_id"):
            table.add_row("Audio ID", upload_data["audio_id"])
        if upload_data.get("audio_url"):
            table.add_row("Audio URL", upload_data["audio_url"])

        console.print(
            Panel(
                table,
                title="[bold green]Upload Result[/bold green]",
                border_style="green",
            )
        )
    else:
        print_json(data)


def print_media_result(data: dict[str, Any], title: str = "Media Result") -> None:
    """Print a media (video/wav) result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    media_data = data.get("data", {})

    lines = [
        f"[bold]Task ID:[/bold] {task_id}",
        f"[bold]Trace ID:[/bold] {trace_id}",
    ]

    if isinstance(media_data, dict):
        if media_data.get("video_url"):
            lines.append(f"[bold]Video URL:[/bold] {media_data['video_url']}")
        if media_data.get("audio_url"):
            lines.append(f"[bold]Audio URL:[/bold] {media_data['audio_url']}")
        if media_data.get("url"):
            lines.append(f"[bold]URL:[/bold] {media_data['url']}")

    console.print(
        Panel(
            "\n".join(lines),
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
        )
    )


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    tasks = data.get("data", [])

    if isinstance(tasks, list):
        for task_data in tasks:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")

            for key in ["id", "status", "state", "audio_url", "video_url", "model_name",
                        "created_at"]:
                if task_data.get(key):
                    table.add_row(key.replace("_", " ").title(), str(task_data[key]))

            console.print(table)
            console.print()
    elif isinstance(tasks, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")

        for key in ["id", "status", "state", "audio_url", "video_url", "model_name",
                    "created_at"]:
            if tasks.get(key):
                table.add_row(key.replace("_", " ").title(), str(tasks[key]))

        console.print(table)


def print_models() -> None:
    """Print available Producer models."""
    table = Table(title="Available Producer Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    notes = {
        "FUZZ-2.0 Pro": "Latest Pro model, best quality",
        "FUZZ-2.0": "Standard model (default)",
        "FUZZ-2.0 Raw": "Raw output model",
        "FUZZ-1.1 Pro": "V1.1 Pro model",
        "FUZZ-1.0 Pro": "V1.0 Pro model",
        "FUZZ-1.0": "V1.0 standard model",
        "FUZZ-1.1": "V1.1 standard model",
        "FUZZ-0.8": "Legacy model",
    }

    for model in PRODUCER_MODELS:
        table.add_row(model, notes.get(model, ""))

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL}[/dim]")

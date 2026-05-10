"""Rich terminal output formatting for Fish CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available TTS models
FISH_TTS_MODELS = ["s1", "s2-pro"]
DEFAULT_TTS_MODEL = "s2-pro"

# Available audio formats
FISH_AUDIO_FORMATS = ["mp3", "wav", "pcm", "opus"]
DEFAULT_AUDIO_FORMAT = "mp3"

# Available MP3 bitrates
FISH_MP3_BITRATES = [64, 128, 192]

# Available latency modes
FISH_LATENCY_MODES = ["normal", "balanced"]
DEFAULT_LATENCY_MODE = "normal"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_tts_result(data: dict[str, Any]) -> None:
    """Print TTS synthesis result in a rich format."""
    task_id = data.get("task_id", "")
    audio_url = data.get("audio_url", "")

    if task_id and not audio_url:
        # Async mode — task submitted
        console.print(
            Panel(
                f"[bold]Task ID:[/bold] {task_id}",
                title="[bold green]TTS Task Submitted[/bold green]",
                border_style="green",
            )
        )
        console.print(
            "[yellow]Audio is being generated. Use 'fish task' to check status.[/yellow]"
        )
        return

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")

    if audio_url:
        table.add_row("Audio URL", audio_url)
    if task_id:
        table.add_row("Task ID", task_id)
    for key in ["trace_id", "state", "created_at"]:
        if data.get(key):
            table.add_row(key.replace("_", " ").title(), str(data[key]))

    console.print(
        Panel(
            table,
            title="[bold green]TTS Result[/bold green]",
            border_style="green",
        )
    )


def print_voice_list(data: dict[str, Any]) -> None:
    """Print a list of voice models in a rich table."""
    total = data.get("total", 0)
    items = data.get("items", [])

    table = Table(title=f"Voice Models (total: {total})")
    table.add_column("ID", style="bold cyan", no_wrap=True)
    table.add_column("Title")
    table.add_column("Type")
    table.add_column("State")
    table.add_column("Languages")
    table.add_column("Visibility")

    for item in items:
        languages = ", ".join(item.get("languages", []))
        table.add_row(
            item.get("_id", ""),
            item.get("title", ""),
            item.get("type", ""),
            item.get("state", ""),
            languages,
            item.get("visibility", ""),
        )

    console.print(table)


def print_voice_detail(data: dict[str, Any]) -> None:
    """Print a single voice model detail."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=18)
    table.add_column("Value")

    fields = [
        ("_id", "ID"),
        ("title", "Title"),
        ("type", "Type"),
        ("state", "State"),
        ("train_mode", "Train Mode"),
        ("visibility", "Visibility"),
        ("description", "Description"),
        ("created_at", "Created"),
        ("updated_at", "Updated"),
    ]
    for key, label in fields:
        value = data.get(key)
        if value:
            table.add_row(label, str(value))

    languages = ", ".join(data.get("languages", []))
    if languages:
        table.add_row("Languages", languages)

    tags = ", ".join(data.get("tags", []))
    if tags:
        table.add_row("Tags", tags)

    author = data.get("author", {})
    if author:
        table.add_row("Author", author.get("name", author.get("nickname", "")))

    console.print(
        Panel(
            table,
            title="[bold green]Voice Model[/bold green]",
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

            for key in ["id", "status", "state", "audio_url", "created_at"]:
                if task_data.get(key):
                    table.add_row(key.replace("_", " ").title(), str(task_data[key]))

            console.print(table)
            console.print()
    elif isinstance(tasks, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")

        for key in ["id", "status", "state", "audio_url", "created_at"]:
            if tasks.get(key):
                table.add_row(key.replace("_", " ").title(), str(tasks[key]))

        console.print(table)

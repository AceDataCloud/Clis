"""Rich terminal output formatting for Fish CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available Fish TTS models
FISH_TTS_MODELS = [
    "s2-pro",
    "s2.1-pro",
    "s1",
]

DEFAULT_TTS_MODEL = "s2-pro"

# Available audio formats
AUDIO_FORMATS = ["mp3", "wav", "opus", "pcm"]

DEFAULT_AUDIO_FORMAT = "mp3"

# Available latency modes
LATENCY_MODES = ["normal", "balanced"]

DEFAULT_LATENCY = "normal"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_tts_result(data: dict[str, Any]) -> None:
    """Print a TTS generation result."""
    task_id = data.get("task_id")
    audio_url = data.get("audio_url")
    started_at = data.get("started_at")

    if task_id and not audio_url:
        # Async response
        content = f"[bold]Task ID:[/bold] {task_id}"
        if started_at:
            content += f"\n[bold]Started At:[/bold] {started_at}"
        console.print(
            Panel(
                content,
                title="[bold green]TTS Task Submitted[/bold green]",
                border_style="green",
            )
        )
        console.print("[dim]Use 'fish task <task_id>' to check status.[/dim]")
    elif audio_url:
        content = f"[bold]Audio URL:[/bold] {audio_url}"
        latency_ms = data.get("latency_ms")
        if latency_ms:
            content += f"\n[bold]Latency:[/bold] {latency_ms}ms"
        console.print(
            Panel(
                content,
                title="[bold green]TTS Generation Result[/bold green]",
                border_style="green",
            )
        )
    else:
        console.print("[yellow]No audio URL available yet.[/yellow]")


def print_model_list(data: dict[str, Any]) -> None:
    """Print a list of fish voice models."""
    items = data.get("items", [])
    total = data.get("total", len(items))

    table = Table(title=f"Fish Voice Models (total: {total})")
    table.add_column("ID", style="bold cyan")
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


def print_model_detail(data: dict[str, Any]) -> None:
    """Print details of a single fish voice model."""
    table = Table(title="Fish Voice Model Detail", show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=20)
    table.add_column("Value")

    fields = [
        ("ID", "_id"),
        ("Title", "title"),
        ("Description", "description"),
        ("Type", "type"),
        ("State", "state"),
        ("Train Mode", "train_mode"),
        ("Languages", None),
        ("Visibility", "visibility"),
        ("Created At", "created_at"),
        ("Updated At", "updated_at"),
    ]

    for label, key in fields:
        if key == "Languages":
            value = ", ".join(data.get("languages", []))
        elif key:
            value = str(data.get(key, ""))
        else:
            value = ""

        if value:
            table.add_row(label, value)

    console.print(table)


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result."""
    task_id = data.get("id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Task Result[/bold green]",
            border_style="green",
        )
    )

    response = data.get("response", {})
    if response:
        inner_data = response.get("data", [])
        if isinstance(inner_data, list) and inner_data:
            item = inner_data[0]
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            if item.get("audio_url"):
                table.add_row("Audio URL", item["audio_url"])
            if item.get("status"):
                table.add_row("Status", item["status"])
            console.print(table)
        elif isinstance(inner_data, dict):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            if inner_data.get("audio_url"):
                table.add_row("Audio URL", inner_data["audio_url"])
            if inner_data.get("status"):
                table.add_row("Status", inner_data["status"])
            console.print(table)


def print_tasks_batch_result(data: dict[str, Any]) -> None:
    """Print batch task query result."""
    items = data.get("items", [])
    count = data.get("count", len(items))
    console.print(f"[bold]Batch task results: {count} tasks[/bold]")

    for item in items:
        print_task_result(item)
        console.print()


def print_tts_models() -> None:
    """Print available Fish TTS models."""
    table = Table(title="Available Fish TTS Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    table.add_row("s2-pro", "Fish Audio S2 Pro (default)")
    table.add_row("s2.1-pro", "Fish Audio S2.1 Pro")
    table.add_row("s1", "Fish Audio S1")

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_TTS_MODEL}[/dim]")

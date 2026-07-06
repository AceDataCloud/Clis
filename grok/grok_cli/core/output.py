"""Rich terminal output formatting for Grok CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available Grok chat models
GROK_CHAT_MODELS = [
    "grok-4",
    "grok-3",
]

DEFAULT_CHAT_MODEL = "grok-4"

# Available Grok video models
GROK_VIDEO_MODELS = [
    "grok-imagine-video-1.5-fast",
    "grok-imagine-video-1.5",
]

DEFAULT_VIDEO_MODEL = "grok-imagine-video-1.5-fast"

# Available aspect ratios for video generation
ASPECT_RATIOS = [
    "1:1",
    "16:9",
    "9:16",
    "4:3",
    "3:4",
    "3:2",
    "2:3",
]

# Available resolutions for video generation
RESOLUTIONS = [
    "480p",
    "720p",
    "1080p",
]

DEFAULT_RESOLUTION = "480p"

# Available reasoning efforts
REASONING_EFFORTS = ["minimal", "low", "medium", "high"]

DEFAULT_REASONING_EFFORT = "medium"

# Available service tiers
SERVICE_TIERS = ["auto", "default", "flex", "scale", "priority"]

DEFAULT_SERVICE_TIER = "auto"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_chat_result(data: dict[str, Any]) -> None:
    """Print a chat completion result."""
    choices = data.get("choices", [])
    if choices:
        for i, choice in enumerate(choices, 1):
            message = choice.get("message", {})
            content = message.get("content", "")
            role = message.get("role", "assistant")
            finish_reason = choice.get("finish_reason", "")
            title = (
                f"[bold green]Response #{i}[/bold green]"
                if len(choices) > 1
                else "[bold green]Response[/bold green]"
            )
            console.print(
                Panel(
                    content or "[dim](empty)[/dim]",
                    title=title,
                    subtitle=(
                        f"[dim]{role} \u00b7 {finish_reason}[/dim]"
                        if finish_reason
                        else f"[dim]{role}[/dim]"
                    ),
                    border_style="green",
                )
            )
    else:
        console.print("[yellow]No response content available.[/yellow]")

    usage = data.get("usage", {})
    if usage:
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="dim")
        table.add_column("Value", style="dim")
        if usage.get("prompt_tokens"):
            table.add_row("Prompt tokens", str(usage["prompt_tokens"]))
        if usage.get("completion_tokens"):
            table.add_row("Completion tokens", str(usage["completion_tokens"]))
        if usage.get("total_tokens"):
            table.add_row("Total tokens", str(usage["total_tokens"]))
        console.print(table)


def print_video_result(data: dict[str, Any]) -> None:
    """Print video generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Video Generation Result[/bold green]",
            border_style="green",
        )
    )

    item = data.get("data", {})
    if not item:
        console.print("[yellow]No data available yet. Use 'task' to check status.[/yellow]")
        return

    if isinstance(item, dict):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        if item.get("task_id"):
            table.add_row("Task ID", item["task_id"])
        if item.get("status"):
            table.add_row("Status", item["status"])
        if item.get("video_url"):
            table.add_row("Video URL", item["video_url"])
        console.print(table)


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
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
        inner = response.get("data", {})
        if isinstance(inner, dict):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            if inner.get("task_id"):
                table.add_row("Task ID", inner["task_id"])
            if inner.get("status"):
                table.add_row("Status", inner["status"])
            if inner.get("video_url"):
                table.add_row("Video URL", inner["video_url"])
            console.print(table)


def print_chat_models() -> None:
    """Print available Grok chat models."""
    table = Table(title="Available Grok Chat Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    table.add_row("grok-4", "Latest Grok model (default)")
    table.add_row("grok-3", "Grok 3")

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_CHAT_MODEL}[/dim]")


def print_video_models() -> None:
    """Print available Grok video models."""
    table = Table(title="Available Grok Video Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    table.add_row("grok-imagine-video-1.5-fast", "Grok Imagine Video 1.5 Fast (default)")
    table.add_row("grok-imagine-video-1.5", "Grok Imagine Video 1.5")

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_VIDEO_MODEL}[/dim]")

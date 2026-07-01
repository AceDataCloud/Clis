"""Rich terminal output formatting for Gemini CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available Gemini chat models
GEMINI_CHAT_MODELS = [
    "gemini-3.1-pro",
    "gemini-3.0-pro",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-flash-image",
    "gemini-3-pro-image",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-image",
    "gemini-2.0-flash",
]

DEFAULT_CHAT_MODEL = "gemini-2.5-flash"

# Available Gemini video models
GEMINI_VIDEO_MODELS = [
    "omni-flash",
]

DEFAULT_VIDEO_MODEL = "omni-flash"

# Available aspect ratios for video
ASPECT_RATIOS = ["16:9", "9:16"]
DEFAULT_ASPECT_RATIO = "16:9"


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
    """Print a video generation result."""
    task_data = data.get("data", {})

    if isinstance(task_data, list) and task_data:
        task_data = task_data[0]

    if isinstance(task_data, dict):
        task_id = task_data.get("id", task_data.get("task_id", ""))
        state = task_data.get("state", task_data.get("status", ""))
        video_url = task_data.get("video_url", "")
        if not video_url:
            videos = task_data.get("videos", [])
            if videos:
                video_url = videos[0].get("url", "")

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan")
        table.add_column("Value")
        if task_id:
            table.add_row("Task ID", str(task_id))
        if state:
            table.add_row("State", str(state))
        if video_url:
            table.add_row("Video URL", str(video_url))
        console.print(table)
    else:
        console.print("[yellow]No video result available.[/yellow]")


def print_task_result(data: dict[str, Any]) -> None:
    """Print a task query result."""
    print_video_result(data)


def print_models() -> None:
    """Print available Gemini models."""
    table = Table(title="Available Gemini Chat Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Notes")

    table.add_row("gemini-3.1-pro", "Latest Gemini Pro model")
    table.add_row("gemini-3.0-pro", "Gemini 3.0 Pro")
    table.add_row("gemini-3.5-flash", "Gemini 3.5 Flash")
    table.add_row("gemini-3-flash-preview", "Gemini 3 Flash Preview")
    table.add_row("gemini-3.1-flash-lite-preview", "Gemini 3.1 Flash Lite Preview")
    table.add_row("gemini-3.1-flash-image", "Gemini 3.1 Flash Image")
    table.add_row("gemini-3-pro-image", "Gemini 3 Pro Image")
    table.add_row("gemini-2.5-pro", "Gemini 2.5 Pro")
    table.add_row("gemini-2.5-flash", "Gemini 2.5 Flash (default)")
    table.add_row("gemini-2.5-flash-lite", "Gemini 2.5 Flash Lite")
    table.add_row("gemini-2.5-flash-image", "Gemini 2.5 Flash Image")
    table.add_row("gemini-2.0-flash", "Gemini 2.0 Flash")

    console.print(table)
    console.print(f"\n[dim]Default chat model: {DEFAULT_CHAT_MODEL}[/dim]")

    video_table = Table(title="Available Gemini Video Models")
    video_table.add_column("Model", style="bold cyan")
    video_table.add_column("Notes")

    video_table.add_row("omni-flash", "Gemini video generation model (default)")

    console.print(video_table)
    console.print(f"\n[dim]Default video model: {DEFAULT_VIDEO_MODEL}[/dim]")

"""Rich terminal output formatting for Maestro CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available actions
MAESTRO_ACTIONS = [
    "generate",
    "remix",
    "edit",
    "extend",
]

DEFAULT_ACTION = "generate"

# Available aspect ratios
ASPECT_RATIOS = [
    "9:16",
    "16:9",
    "1:1",
]

DEFAULT_ASPECT_RATIO = "9:16"

# Available quality tiers
QUALITY_TIERS = [
    "draft",
    "standard",
    "premium",
]

DEFAULT_QUALITY = "standard"

# Available scenarios
SCENARIOS = [
    "auto",
    "narrated",
    "drama",
    "avatar",
    "motion",
    "slideshow",
]

DEFAULT_SCENARIO = "auto"

# Available styles
STYLES = [
    "auto",
    "cinematic",
    "glass",
    "luxury",
    "swiss",
    "modern",
    "editorial",
    "warm",
    "vibrant",
    "neon",
    "mono",
    "pastel",
    "bold",
    "industrial",
    "futuristic",
    "retro",
]

DEFAULT_STYLE = "auto"

# Available voices
VOICES = [
    "auto",
    "warm-female",
    "bright-female",
    "anchor-female",
    "clean-female",
    "calm-male",
    "deep-male",
    "documentary-male",
    "energetic-male",
    "storyteller-male",
]

DEFAULT_VOICE = "auto"

# Default output language
DEFAULT_LANGS = ["zh-cn"]

# Default duration (seconds)
DEFAULT_DURATION = 30


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_video_result(data: dict[str, Any]) -> None:
    """Print video creation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Maestro Video Result[/bold green]",
            border_style="green",
        )
    )

    if not data.get("task_id"):
        console.print("[yellow]No task ID available yet.[/yellow]")
    else:
        console.print("[dim]Use 'maestro task' to check job status.[/dim]")


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    task_id = data.get("id", "N/A")
    status = data.get("status", "N/A")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")

    if task_id != "N/A":
        table.add_row("Task ID", str(task_id))
    if status != "N/A":
        table.add_row("Status", str(status))

    created_at = data.get("created_at")
    if created_at:
        table.add_row("Created At", str(created_at))

    started_at = data.get("started_at")
    if started_at:
        table.add_row("Started At", str(started_at))

    finished_at = data.get("finished_at")
    if finished_at:
        table.add_row("Finished At", str(finished_at))

    elapsed = data.get("elapsed")
    if elapsed is not None:
        table.add_row("Elapsed", f"{elapsed}s")

    console.print(table)

    response = data.get("response", {})
    if response:
        resp_data = response.get("data", {})
        if isinstance(resp_data, dict):
            variants = resp_data.get("variants", [])
            if variants:
                console.print("\n[bold]Output Variants:[/bold]")
                for v in variants:
                    vtable = Table(show_header=False, box=None, padding=(0, 2))
                    vtable.add_column("Field", style="cyan", width=15)
                    vtable.add_column("Value")
                    if v.get("lang"):
                        vtable.add_row("Language", v["lang"])
                    if v.get("output_url"):
                        vtable.add_row("Video URL", v["output_url"])
                    if v.get("cover_url"):
                        vtable.add_row("Cover URL", v["cover_url"])
                    if v.get("duration") is not None:
                        vtable.add_row("Duration", f"{v['duration']}s")
                    console.print(vtable)


def print_models() -> None:
    """Print available Maestro options."""
    table = Table(title="Available Maestro Scenarios")
    table.add_column("Scenario", style="bold cyan")
    table.add_column("Description")

    scenario_notes = {
        "auto": "AI director chooses from your brief (default)",
        "narrated": "Multi-scene narrated video with real photos + voiceover",
        "drama": "Acted short drama with characters + dialogue (1.35×)",
        "avatar": "Talking-head / digital human (1.15×)",
        "motion": "Abstract kinetic-typography / data / logo motion graphic",
        "slideshow": "Presentation deck / pitch",
    }
    for scenario, note in scenario_notes.items():
        table.add_row(scenario, note)

    console.print(table)
    console.print(f"\n[dim]Default scenario: {DEFAULT_SCENARIO}[/dim]")
    console.print(f"[dim]Default quality: {DEFAULT_QUALITY}[/dim]")
    console.print(f"[dim]Default aspect: {DEFAULT_ASPECT_RATIO}[/dim]")
    console.print(f"[dim]Default duration: {DEFAULT_DURATION}s[/dim]")

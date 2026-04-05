"""Rich terminal output formatting for Midjourney CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available modes
MIDJOURNEY_MODES = ["fast", "relax", "turbo"]
DEFAULT_MODE = "fast"

# Available versions
MIDJOURNEY_VERSIONS = ["5.2", "6", "6.1", "7", "8"]

# Available imagine actions
IMAGINE_ACTIONS = [
    "generate",
    "upscale1",
    "upscale2",
    "upscale3",
    "upscale4",
    "upscale_2x",
    "upscale_4x",
    "variation1",
    "variation2",
    "variation3",
    "variation4",
    "variation_subtle",
    "variation_strong",
    "variation_region",
    "reroll",
    "zoom_out_2x",
    "zoom_out_1_5x",
    "pan_left",
    "pan_right",
    "pan_up",
    "pan_down",
]

# Video modes (relax not supported for video)
VIDEO_MODES = ["fast", "turbo"]
DEFAULT_VIDEO_MODE = "fast"

# Video resolutions
VIDEO_RESOLUTIONS = ["480p", "720p"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_imagine_result(data: dict[str, Any]) -> None:
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

    # Display image info if available
    if data.get("image_url"):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        table.add_row("Image URL", data["image_url"])
        if data.get("image_id"):
            table.add_row("Image ID", data["image_id"])
        if data.get("image_width") and data.get("image_height"):
            table.add_row("Dimensions", f"{data['image_width']}x{data['image_height']}")
        if data.get("actions"):
            table.add_row("Actions", ", ".join(data["actions"]))
        console.print(table)

    # Display sub-images if split
    if data.get("sub_image_urls"):
        console.print("\n[bold]Split Images:[/bold]")
        for i, url in enumerate(data["sub_image_urls"], 1):
            console.print(f"  {i}. {url}")

    if not data.get("image_url") and not data.get("sub_image_urls"):
        console.print("[yellow]No image available yet. Use 'task' to check status.[/yellow]")


def print_edit_result(data: dict[str, Any]) -> None:
    """Print image edit result in a rich format."""
    print_imagine_result(data)


def print_video_result(data: dict[str, Any]) -> None:
    """Print video generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title="[bold green]Video Result[/bold green]",
            border_style="green",
        )
    )

    if data.get("cover_image_url"):
        console.print(f"[bold]Cover Image:[/bold] {data['cover_image_url']}")

    video_urls = data.get("video_urls", [])
    if video_urls:
        for i, url in enumerate(video_urls, 1):
            console.print(f"  Video {i}: {url}")
    else:
        console.print("[yellow]No video available yet. Use 'task' to check status.[/yellow]")


def print_describe_result(data: dict[str, Any]) -> None:
    """Print image description result in a rich format."""
    descriptions = data.get("descriptions", [])
    if descriptions:
        console.print(
            Panel(
                "\n".join(f"[bold]{i}.[/bold] {d}" for i, d in enumerate(descriptions, 1)),
                title="[bold green]Image Descriptions[/bold green]",
                border_style="green",
            )
        )
    else:
        console.print("[yellow]No descriptions returned.[/yellow]")


def print_translate_result(data: dict[str, Any]) -> None:
    """Print translation result in a rich format."""
    translated = data.get("translated_content", data.get("content", ""))
    if translated:
        console.print(
            Panel(
                translated,
                title="[bold green]Translation[/bold green]",
                border_style="green",
            )
        )
    else:
        console.print("[yellow]No translation returned.[/yellow]")


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    # Handle single-task response
    if data.get("image_url") or data.get("video_urls"):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        for key in [
            "task_id",
            "image_id",
            "image_url",
            "image_width",
            "image_height",
            "video_urls",
            "cover_image_url",
            "actions",
        ]:
            val = data.get(key)
            if val:
                if isinstance(val, list):
                    table.add_row(key.replace("_", " ").title(), ", ".join(str(v) for v in val))
                else:
                    table.add_row(key.replace("_", " ").title(), str(val))
        console.print(table)
        return

    # Handle batch response
    items = data.get("items", [])
    if items:
        for item in items:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            for key in ["id", "type", "created_at"]:
                if item.get(key):
                    table.add_row(key.replace("_", " ").title(), str(item[key]))
            resp = item.get("response", {})
            if resp.get("image_url"):
                table.add_row("Image URL", resp["image_url"])
            console.print(table)
            console.print()
        return

    # Generic fallback
    console.print("[yellow]No data available.[/yellow]")


def print_seed_result(data: dict[str, Any]) -> None:
    """Print seed result in a rich format."""
    seed = data.get("seed", "N/A")
    console.print(
        Panel(
            f"[bold]Seed:[/bold] {seed}",
            title="[bold green]Image Seed[/bold green]",
            border_style="green",
        )
    )


def print_modes() -> None:
    """Print available Midjourney modes."""
    table = Table(title="Available Modes")
    table.add_column("Mode", style="bold cyan")
    table.add_column("Speed")
    table.add_column("Cost")
    table.add_column("Notes")

    table.add_row("fast", "Fast", "Standard", "Recommended for most use cases (default)")
    table.add_row("turbo", "Fastest", "Higher", "Faster but uses more credits")
    table.add_row("relax", "Slow", "Lower", "Slower but cheaper")

    console.print(table)
    console.print(f"\n[dim]Default mode: {DEFAULT_MODE}[/dim]")


def print_versions() -> None:
    """Print available Midjourney versions."""
    table = Table(title="Available Midjourney Versions")
    table.add_column("Version", style="bold cyan")
    table.add_column("Notes")

    table.add_row("5.2", "Stable, well-tested")
    table.add_row("6", "Improved prompt understanding")
    table.add_row("6.1", "Enhanced detail and coherence")
    table.add_row("7", "Better composition and realism")
    table.add_row("8", "Latest V8 Alpha — HD and ultra quality support")

    console.print(table)
    console.print("\n[dim]Leave unset to use Midjourney's default version.[/dim]")

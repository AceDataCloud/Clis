"""Rich terminal output formatting for QRArt CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available QR content types
QR_TYPES = ["link", "text", "email", "phone", "sms"]
DEFAULT_TYPE = "link"

# Available presets
PRESETS = [
    "sunset",
    "floral",
    "snowflakes",
    "feathers",
    "raindrops",
    "ultra-realism",
    "epic-realms",
    "intricate-studio",
    "symmetric-masterpiece",
    "luminous-highway",
    "celestial-journey",
    "neon-mech",
    "ethereal-low-poly",
    "golden-vista",
    "cinematic-expanse",
    "cinematic-warm",
    "desolate-wilderness",
    "vibrant-palette",
    "enigmatic-journey",
    "timeless-cinematic",
    "regal-galaxy",
    "illustrious-canvas",
    "expressive-mural",
    "serene-haze",
]

# Available patterns
PATTERNS = [
    "custom", "s1", "s2", "s3", "rd1", "rd2", "rd3",
    "d1", "d2", "d3", "r1", "r2", "r3", "c1", "c2", "c3",
    "sq1", "sq2", "sq3",
]

# Available pixel styles
PIXEL_STYLES = ["square", "rounded", "dot", "squircle", "row", "column"]

# Available marker shapes
MARKER_SHAPES = ["square", "circle", "plus", "box", "octagon", "random", "tiny-plus"]

# Available sub-markers
SUB_MARKERS = ["square", "circle", "box", "random", "plus"]

# Available positions
POSITIONS = [
    "center", "top", "right", "bottom", "left",
    "top-left", "top-right", "bottom-left", "bottom-right",
]

# Available aspect ratios
ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4"]
DEFAULT_ASPECT_RATIO = "1:1"

# Available rotations
ROTATIONS = [0, 90, 180, 270]

# Available error correction levels
ECL_VALUES = ["L", "M", "Q", "H"]

# Available padding levels
PADDING_LEVELS = [0, 5, 10, 15, 20]

# Available padding noise values
PADDING_NOISE_VALUES = [0, 0.25, 0.5, 0.75, 1]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_qr_result(data: dict[str, Any]) -> None:
    """Print QR code generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    info_lines = [
        f"[bold]Task ID:[/bold] {task_id}",
        f"[bold]Trace ID:[/bold] {trace_id}",
    ]
    if data.get("state"):
        info_lines.append(f"[bold]State:[/bold] {data['state']}")
    if data.get("image_url"):
        info_lines.append(f"[bold]Image URL:[/bold] {data['image_url']}")

    console.print(
        Panel(
            "\n".join(info_lines),
            title="[bold green]QR Art Result[/bold green]",
            border_style="green",
        )
    )


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")

    for key in ["id", "task_id", "state", "progress", "image_url"]:
        if data.get(key) is not None:
            table.add_row(key.replace("_", " ").title(), str(data[key]))

    console.print(table)


def print_presets() -> None:
    """Print available style presets."""
    table = Table(title="Available Style Presets")
    table.add_column("Preset", style="bold cyan")

    for preset in PRESETS:
        table.add_row(preset)

    console.print(table)

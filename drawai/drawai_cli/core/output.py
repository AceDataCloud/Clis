"""Rich terminal output formatting for DrawAI CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available modes
MODES = ["fast", "relax"]
DEFAULT_MODE = "fast"

# Available templates
TEMPLATES = [
    "male_portrait",
    "male_portrait2",
    "kindergarten",
    "logo_tshirt",
    "wedding",
    "business_photo",
    "bob_suit",
    "female_portrait",
]
DEFAULT_TEMPLATE = "business_photo"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_headshot_result(data: dict[str, Any]) -> None:
    """Print headshot generation result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    info_lines = [
        f"[bold]Task ID:[/bold] {task_id}",
        f"[bold]Trace ID:[/bold] {trace_id}",
    ]
    if data.get("state"):
        info_lines.append(f"[bold]State:[/bold] {data['state']}")

    images = data.get("images") or data.get("data", {})
    if isinstance(images, list):
        for i, img in enumerate(images, 1):
            url = img if isinstance(img, str) else img.get("url", "")
            if url:
                info_lines.append(f"[bold]Image {i}:[/bold] {url}")
    elif isinstance(images, dict):
        for key in ["image_url", "url"]:
            if images.get(key):
                info_lines.append(f"[bold]Image URL:[/bold] {images[key]}")

    console.print(
        Panel(
            "\n".join(info_lines),
            title="[bold green]AI Headshot Result[/bold green]",
            border_style="green",
        )
    )


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result in a rich format."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")

    for key in ["task_id", "state", "progress"]:
        if data.get(key) is not None:
            table.add_row(key.replace("_", " ").title(), str(data[key]))

    console.print(table)


def print_templates() -> None:
    """Print available templates."""
    table = Table(title="Available Templates")
    table.add_column("Template", style="bold cyan")
    table.add_column("Description")

    descriptions = {
        "male_portrait": "Male portrait style",
        "male_portrait2": "Male portrait style 2",
        "kindergarten": "Kindergarten photo style",
        "logo_tshirt": "Logo T-shirt style",
        "wedding": "Wedding photo style",
        "business_photo": "Business/professional photo (default)",
        "bob_suit": "Bob suit style",
        "female_portrait": "Female portrait style",
    }
    for template in TEMPLATES:
        table.add_row(template, descriptions.get(template, ""))

    console.print(table)
    console.print(f"\n[dim]Default template: {DEFAULT_TEMPLATE}[/dim]")

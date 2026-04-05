"""Rich terminal output formatting for AceDataCloud CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Service catalog
SERVICES = {
    "flux": {"type": "Image", "description": "Flux AI image generation & editing"},
    "midjourney": {"type": "Image", "description": "Midjourney image generation"},
    "seedream": {"type": "Image", "description": "Seedream image generation"},
    "nanobanana": {"type": "Image", "description": "NanoBanana image generation & editing"},
    "suno": {"type": "Music", "description": "Suno AI music generation"},
    "luma": {"type": "Video", "description": "Luma Dream Machine video generation"},
    "sora": {"type": "Video", "description": "OpenAI Sora video generation"},
    "veo": {"type": "Video", "description": "Google Veo video generation"},
    "seedance": {"type": "Video", "description": "Seedance video generation"},
    "serp": {"type": "Search", "description": "Google Search (SERP)"},
}


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_result(data: dict[str, Any], result_type: str = "Result") -> None:
    """Print a generic API result."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")

    console.print(
        Panel(
            f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
            title=f"[bold green]{result_type}[/bold green]",
            border_style="green",
        )
    )

    items = data.get("data", [])
    if isinstance(items, list) and items:
        for i, item in enumerate(items, 1):
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            table.add_row("Item", f"#{i}")
            for key in ["image_url", "video_url", "audio_url", "model", "model_name", "created_at"]:
                if item.get(key):
                    table.add_row(key.replace("_", " ").title(), str(item[key]))
            console.print(table)
            console.print()
    else:
        console.print("[yellow]No data available yet. Use 'adc task' to check status.[/yellow]")


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result."""
    items = data.get("data", [])
    if isinstance(items, list) and items:
        for item in items:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Field", style="bold cyan", width=15)
            table.add_column("Value")
            for key in [
                "image_url",
                "video_url",
                "audio_url",
                "model",
                "model_name",
                "state",
                "status",
                "created_at",
            ]:
                if item.get(key):
                    table.add_row(key.replace("_", " ").title(), str(item[key]))
            console.print(table)
            console.print()
        return

    console.print("[yellow]No data available.[/yellow]")


def print_search_result(data: dict[str, Any]) -> None:
    """Print search results."""
    # Knowledge graph
    kg = data.get("knowledge_graph")
    if kg:
        title = kg.get("title", "")
        description = kg.get("description", "")
        if title:
            console.print(
                Panel(
                    f"[bold]{title}[/bold]\n{description}"
                    if description
                    else f"[bold]{title}[/bold]",
                    title="[bold blue]Knowledge Graph[/bold blue]",
                    border_style="blue",
                )
            )

    # Organic results
    organic = data.get("organic", [])
    if organic:
        table = Table(title="Search Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Title", style="bold cyan", max_width=50)
        table.add_column("URL", style="dim", max_width=40)

        for i, item in enumerate(organic, 1):
            table.add_row(str(i), item.get("title", "N/A"), item.get("link", "N/A"))

        console.print(table)

    # News
    news = data.get("news", [])
    if news:
        table = Table(title="News Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Title", style="bold cyan", max_width=50)
        table.add_column("Source", max_width=20)

        for i, item in enumerate(news, 1):
            table.add_row(str(i), item.get("title", "N/A"), item.get("source", "N/A"))

        console.print(table)

    if not any([organic, news, kg]):
        console.print("[yellow]No results found.[/yellow]")


def print_services() -> None:
    """Print available services."""
    table = Table(title="AceDataCloud Services")
    table.add_column("Service", style="bold cyan")
    table.add_column("Type")
    table.add_column("Description")
    table.add_column("CLI")

    for name, info in SERVICES.items():
        table.add_row(name, info["type"], info["description"], f"adc {name.split('-')[0]}")

    console.print(table)
    console.print("\n[dim]Use 'adc <service> --help' for service-specific commands.[/dim]")

"""Rich terminal output formatting for SERP CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available search types
SEARCH_TYPES = ["search", "images", "news", "maps", "places", "videos"]
DEFAULT_SEARCH_TYPE = "search"

# Common time ranges
TIME_RANGES = ["qdr:h", "qdr:d", "qdr:w", "qdr:m"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_search_result(data: dict[str, Any]) -> None:
    """Print search results in a rich format."""
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

    # Answer box
    answer = data.get("answer_box")
    if answer:
        snippet = answer.get("snippet") or answer.get("answer") or ""
        if snippet:
            console.print(
                Panel(
                    snippet,
                    title="[bold green]Answer[/bold green]",
                    border_style="green",
                )
            )

    # Organic results
    organic = data.get("organic", [])
    if organic:
        table = Table(title="Search Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Title", style="bold cyan", max_width=50)
        table.add_column("URL", style="dim", max_width=40)
        table.add_column("Snippet", max_width=60)

        for i, item in enumerate(organic, 1):
            table.add_row(
                str(i),
                item.get("title", "N/A"),
                item.get("link", "N/A"),
                (item.get("snippet", "")[:80] + "...")
                if len(item.get("snippet", "")) > 80
                else item.get("snippet", ""),
            )

        console.print(table)

    # Images
    images = data.get("images", [])
    if images:
        table = Table(title="Image Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Title", style="bold cyan", max_width=40)
        table.add_column("URL", max_width=60)

        for i, item in enumerate(images, 1):
            table.add_row(
                str(i),
                item.get("title", "N/A"),
                item.get("original", item.get("link", "N/A")),
            )

        console.print(table)

    # News
    news = data.get("news", [])
    if news:
        table = Table(title="News Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Title", style="bold cyan", max_width=50)
        table.add_column("Source", max_width=20)
        table.add_column("Date", max_width=20)

        for i, item in enumerate(news, 1):
            table.add_row(
                str(i),
                item.get("title", "N/A"),
                item.get("source", "N/A"),
                item.get("date", "N/A"),
            )

        console.print(table)

    # Videos
    videos = data.get("videos", [])
    if videos:
        table = Table(title="Video Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Title", style="bold cyan", max_width=50)
        table.add_column("Source", max_width=20)
        table.add_column("Duration", max_width=10)

        for i, item in enumerate(videos, 1):
            table.add_row(
                str(i),
                item.get("title", "N/A"),
                item.get("source", item.get("channel", "N/A")),
                item.get("duration", "N/A"),
            )

        console.print(table)

    # Places
    places = data.get("places", [])
    if places:
        table = Table(title="Places Results", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Name", style="bold cyan", max_width=30)
        table.add_column("Address", max_width=40)
        table.add_column("Rating", max_width=10)

        for i, item in enumerate(places, 1):
            rating = item.get("rating", "")
            rating_str = f"{rating}" if rating else "N/A"
            table.add_row(
                str(i),
                item.get("title", item.get("name", "N/A")),
                item.get("address", "N/A"),
                rating_str,
            )

        console.print(table)

    # People also ask
    paa = data.get("people_also_ask", [])
    if paa:
        console.print("\n[bold]People Also Ask:[/bold]")
        for item in paa:
            question = item.get("question", "")
            if question:
                console.print(f"  [cyan]?[/cyan] {question}")

    # Related searches
    related = data.get("related_searches", [])
    if related:
        console.print("\n[bold]Related Searches:[/bold]")
        for item in related:
            query = item.get("query", "")
            if query:
                console.print(f"  [dim]>[/dim] {query}")

    # If nothing was printed, show a message
    if not any([organic, images, news, videos, places, kg, answer]):
        console.print("[yellow]No results found.[/yellow]")


def print_search_types() -> None:
    """Print available search types."""
    table = Table(title="Available Search Types")
    table.add_column("Type", style="bold cyan")
    table.add_column("Description")
    table.add_column("Use Case")

    table.add_row("search", "Regular web search (default)", "General queries, finding websites")
    table.add_row("images", "Image search", "Finding pictures, photos, graphics")
    table.add_row("news", "News articles", "Current events, recent news")
    table.add_row("maps", "Map/location results", "Finding locations on maps")
    table.add_row("places", "Local businesses and places", "Restaurants, shops, services")
    table.add_row("videos", "Video results", "YouTube, video content")

    console.print(table)

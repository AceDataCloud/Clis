"""Rich terminal output formatting for WebExtrator CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Valid wait_until values
WAIT_UNTIL_OPTIONS = [
    "load",
    "domcontentloaded",
    "networkidle",
    "commit",
]

# Valid resource types to block
BLOCK_RESOURCE_TYPES = [
    "image",
    "font",
    "media",
    "stylesheet",
    "xhr",
    "fetch",
]

# Valid expected page types for extract
EXPECTED_TYPES = [
    "product",
    "article",
    "general",
]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_extract_result(data: dict[str, Any]) -> None:
    """Print extract result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    elapsed = data.get("elapsed", "")

    lines = [
        f"[bold]Task ID:[/bold] {task_id}",
        f"[bold]Trace ID:[/bold] {trace_id}",
    ]
    if elapsed:
        lines.append(f"[bold]Elapsed:[/bold] {elapsed}s")

    inner_data = data.get("data", {})
    if isinstance(inner_data, dict):
        url = inner_data.get("url", "")
        title = inner_data.get("title", "")
        content_type = inner_data.get("contentType", "")
        description = inner_data.get("description", "")

        if url:
            lines.append(f"[bold]URL:[/bold] {url}")
        if title:
            lines.append(f"[bold]Title:[/bold] {title}")
        if content_type:
            lines.append(f"[bold]Type:[/bold] {content_type}")
        if description:
            lines.append(f"[bold]Description:[/bold] {description[:120]}{'...' if len(description) > 120 else ''}")

    console.print(
        Panel(
            "\n".join(lines),
            title="[bold green]Extract Result[/bold green]",
            border_style="green",
        )
    )


def print_render_result(data: dict[str, Any]) -> None:
    """Print render result in a rich format."""
    task_id = data.get("task_id", "N/A")
    trace_id = data.get("trace_id", "N/A")
    elapsed = data.get("elapsed", "")

    lines = [
        f"[bold]Task ID:[/bold] {task_id}",
        f"[bold]Trace ID:[/bold] {trace_id}",
    ]
    if elapsed:
        lines.append(f"[bold]Elapsed:[/bold] {elapsed}s")

    inner_data = data.get("data", {})
    if isinstance(inner_data, dict):
        url = inner_data.get("url", "")
        final_url = inner_data.get("finalUrl", "")
        title = inner_data.get("title", "")
        status = inner_data.get("status", "")

        if url:
            lines.append(f"[bold]URL:[/bold] {url}")
        if final_url and final_url != url:
            lines.append(f"[bold]Final URL:[/bold] {final_url}")
        if title:
            lines.append(f"[bold]Title:[/bold] {title}")
        if status:
            lines.append(f"[bold]HTTP Status:[/bold] {status}")

        html = inner_data.get("html", "")
        if html:
            lines.append(f"[bold]HTML length:[/bold] {len(html)} chars")

    console.print(
        Panel(
            "\n".join(lines),
            title="[bold green]Render Result[/bold green]",
            border_style="green",
        )
    )


def print_task_result(data: dict[str, Any]) -> None:
    """Print a single task result."""
    if not data:
        console.print("[yellow]No task found.[/yellow]")
        return

    task_id = data.get("task_id") or data.get("id", "")
    trace_id = data.get("trace_id", "")
    task_type = data.get("type", "")
    started_at = data.get("started_at", "")
    finished_at = data.get("finished_at", "")
    elapsed = data.get("elapsed", "")

    lines = []
    if task_id:
        lines.append(f"[bold]Task ID:[/bold] {task_id}")
    if trace_id:
        lines.append(f"[bold]Trace ID:[/bold] {trace_id}")
    if task_type:
        lines.append(f"[bold]Type:[/bold] {task_type}")
    if started_at:
        lines.append(f"[bold]Started:[/bold] {started_at}")
    if finished_at:
        lines.append(f"[bold]Finished:[/bold] {finished_at}")
    if elapsed:
        lines.append(f"[bold]Elapsed:[/bold] {elapsed}s")

    response = data.get("response", {})
    if isinstance(response, dict):
        kind = response.get("kind", "")
        title = response.get("title", "")
        if kind:
            lines.append(f"[bold]Kind:[/bold] {kind}")
        if title:
            lines.append(f"[bold]Title:[/bold] {title}")

    console.print(
        Panel(
            "\n".join(lines) or "[dim](empty)[/dim]",
            title="[bold green]Task[/bold green]",
            border_style="green",
        )
    )


def print_task_batch_result(data: dict[str, Any]) -> None:
    """Print a batch of task results."""
    items = data.get("items", [])
    count = data.get("count", len(items))

    if not items:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    console.print(f"[bold]Found {count} task(s):[/bold]")
    for i, item in enumerate(items, 1):
        task_id = item.get("task_id") or item.get("id", "")
        trace_id = item.get("trace_id", "")
        task_type = item.get("type", "")
        started_at = item.get("started_at", "")

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=12)
        table.add_column("Value")
        if task_id:
            table.add_row("Task ID", task_id)
        if trace_id:
            table.add_row("Trace ID", trace_id)
        if task_type:
            table.add_row("Type", task_type)
        if started_at:
            table.add_row("Started", started_at)

        console.print(
            Panel(table, title=f"[bold green]Task #{i}[/bold green]", border_style="green")
        )

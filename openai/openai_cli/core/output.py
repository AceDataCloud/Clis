"""Rich terminal output formatting for OpenAI CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Chat completion models
CHAT_MODELS = [
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-pro",
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-35-turbo-16k",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
]

# Embedding models
EMBEDDING_MODELS = [
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
]

# Image generation/editing models
IMAGE_MODELS = [
    "dall-e-2",
    "dall-e-3",
    "gpt-image-1",
    "gpt-image-1.5",
    "gpt-image-2",
    "nano-banana",
    "nano-banana-2",
    "nano-banana-pro",
]

# Response API models
RESPONSE_MODELS = [
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-pro",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4",
    "gpt-4-all",
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-4-vision-preview",
    "gpt-4.1",
    "gpt-4.1-2025-04-14",
    "gpt-4.1-mini",
    "gpt-4.1-mini-2025-04-14",
    "gpt-4.1-nano",
    "gpt-4.1-nano-2025-04-14",
    "gpt-4.5-preview",
    "gpt-4.5-preview-2025-02-27",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-11-20",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-mini-search-preview",
    "gpt-4o-mini-search-preview-2025-03-11",
    "gpt-4o-search-preview",
    "gpt-4o-search-preview-2025-03-11",
    "gpt-35-turbo-16k",
    "o1",
    "o1-2024-12-17",
    "o1-all",
    "o1-mini",
    "o1-mini-2024-09-12",
    "o1-mini-all",
    "o1-preview",
    "o1-preview-2024-09-12",
    "o1-preview-all",
    "o1-pro",
    "o1-pro-2025-03-19",
    "o1-pro-all",
    "o3",
    "o3-2025-04-16",
    "o3-all",
    "o3-mini",
    "o3-mini-2025-01-31",
    "o3-mini-2025-01-31-high",
    "o3-mini-2025-01-31-low",
    "o3-mini-2025-01-31-medium",
    "o3-mini-all",
    "o3-mini-high",
    "o3-mini-high-all",
    "o3-mini-low",
    "o3-mini-medium",
    "o3-pro",
    "o3-pro-2025-06-10",
    "o4-mini",
    "o4-mini-2025-04-16",
    "o4-mini-all",
    "o4-mini-high-all",
]

DEFAULT_CHAT_MODEL = "gpt-4o-mini"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_IMAGE_MODEL = "dall-e-3"
DEFAULT_RESPONSE_MODEL = "gpt-4o-mini"


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
            title = f"[bold green]Response #{i}[/bold green]" if len(choices) > 1 else "[bold green]Response[/bold green]"
            console.print(
                Panel(
                    content or "[dim](empty)[/dim]",
                    title=title,
                    subtitle=f"[dim]{role} · {finish_reason}[/dim]" if finish_reason else f"[dim]{role}[/dim]",
                    border_style="green",
                )
            )
    else:
        task_id = data.get("task_id", "")
        if task_id:
            console.print(
                Panel(
                    f"[bold]Task ID:[/bold] {task_id}",
                    title="[bold yellow]Queued[/bold yellow]",
                    border_style="yellow",
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


def print_embedding_result(data: dict[str, Any]) -> None:
    """Print an embedding result."""
    embedding_data = data.get("data", [])
    if embedding_data:
        for item in embedding_data:
            embedding = item.get("embedding", [])
            console.print(
                Panel(
                    f"[bold]Dimensions:[/bold] {len(embedding)}\n"
                    f"[bold]Index:[/bold] {item.get('index', 0)}\n"
                    f"[bold]Preview:[/bold] [{', '.join(f'{v:.6f}' for v in embedding[:5])}{'...' if len(embedding) > 5 else ''}]",
                    title="[bold green]Embedding[/bold green]",
                    border_style="green",
                )
            )
    else:
        console.print("[yellow]No embedding data returned.[/yellow]")

    usage = data.get("usage", {})
    if usage:
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="dim")
        table.add_column("Value", style="dim")
        if usage.get("prompt_tokens"):
            table.add_row("Prompt tokens", str(usage["prompt_tokens"]))
        if usage.get("total_tokens"):
            table.add_row("Total tokens", str(usage["total_tokens"]))
        console.print(table)


def print_image_result(data: dict[str, Any]) -> None:
    """Print an image generation/edit result."""
    task_id = data.get("task_id", "")
    trace_id = data.get("trace_id", "")

    image_data = data.get("data", [])
    if image_data:
        for i, item in enumerate(image_data, 1):
            url = item.get("url", "") or item.get("image_url", "")
            b64 = item.get("b64_json", "")
            revised_prompt = item.get("revised_prompt", "")
            parts = []
            if url:
                parts.append(f"[bold]URL:[/bold] {url}")
            if b64:
                parts.append(f"[bold]Base64:[/bold] {b64[:40]}...")
            if revised_prompt:
                parts.append(f"[bold]Revised Prompt:[/bold] {revised_prompt}")
            title = f"[bold green]Image #{i}[/bold green]" if len(image_data) > 1 else "[bold green]Image[/bold green]"
            console.print(
                Panel("\n".join(parts) or "[dim](no URL)[/dim]", title=title, border_style="green")
            )
    elif task_id:
        console.print(
            Panel(
                f"[bold]Task ID:[/bold] {task_id}\n[bold]Trace ID:[/bold] {trace_id}",
                title="[bold yellow]Queued[/bold yellow]",
                border_style="yellow",
            )
        )
    else:
        console.print("[yellow]No image data available yet.[/yellow]")


def print_response_result(data: dict[str, Any]) -> None:
    """Print a Responses API result."""
    output = data.get("output", [])
    if output:
        for item in output:
            item_type = item.get("type", "")
            if item_type == "message":
                content_list = item.get("content", [])
                for content in content_list:
                    text = content.get("text", "")
                    console.print(
                        Panel(
                            text or "[dim](empty)[/dim]",
                            title="[bold green]Response[/bold green]",
                            border_style="green",
                        )
                    )
    else:
        task_id = data.get("task_id", "")
        if task_id:
            console.print(
                Panel(
                    f"[bold]Task ID:[/bold] {task_id}",
                    title="[bold yellow]Queued[/bold yellow]",
                    border_style="yellow",
                )
            )
        else:
            console.print("[yellow]No response content available.[/yellow]")

    usage = data.get("usage", {})
    if usage:
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="dim")
        table.add_column("Value", style="dim")
        if usage.get("input_tokens"):
            table.add_row("Input tokens", str(usage["input_tokens"]))
        if usage.get("output_tokens"):
            table.add_row("Output tokens", str(usage["output_tokens"]))
        if usage.get("total_tokens"):
            table.add_row("Total tokens", str(usage["total_tokens"]))
        console.print(table)


def print_task_result(data: dict[str, Any]) -> None:
    """Print a single task result."""
    if not data:
        console.print("[yellow]No task found.[/yellow]")
        return

    task_id = data.get("id", "")
    trace_id = data.get("trace_id", "")
    task_type = data.get("type", "")
    created_at = data.get("created_at", "")
    finished_at = data.get("finished_at", "")
    duration = data.get("duration", "")

    lines = []
    if task_id:
        lines.append(f"[bold]Task ID:[/bold] {task_id}")
    if trace_id:
        lines.append(f"[bold]Trace ID:[/bold] {trace_id}")
    if task_type:
        lines.append(f"[bold]Type:[/bold] {task_type}")
    if created_at:
        lines.append(f"[bold]Created:[/bold] {created_at}")
    if finished_at:
        lines.append(f"[bold]Finished:[/bold] {finished_at}")
    if duration:
        lines.append(f"[bold]Duration:[/bold] {duration}s")

    response = data.get("response", {})
    if response:
        success = response.get("success", "")
        image_data = response.get("data", [])
        if success is not None:
            lines.append(f"[bold]Success:[/bold] {success}")
        if image_data:
            for i, item in enumerate(image_data, 1):
                url = item.get("url", "") or item.get("image_url", "")
                if url:
                    lines.append(f"[bold]Image {i}:[/bold] {url}")

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
        task_id = item.get("id", "")
        trace_id = item.get("trace_id", "")
        task_type = item.get("type", "")
        created_at = item.get("created_at", "")

        lines = []
        if task_id:
            lines.append(f"[bold]Task ID:[/bold] {task_id}")
        if trace_id:
            lines.append(f"[bold]Trace ID:[/bold] {trace_id}")
        if task_type:
            lines.append(f"[bold]Type:[/bold] {task_type}")
        if created_at:
            lines.append(f"[bold]Created:[/bold] {created_at}")

        console.print(
            Panel(
                "\n".join(lines) or "[dim](empty)[/dim]",
                title=f"[bold green]Task #{i}[/bold green]",
                border_style="green",
            )
        )


def print_models() -> None:
    """Print available models for all endpoints."""
    table = Table(title="Available Chat Completion Models")
    table.add_column("Model", style="bold cyan")
    for model in CHAT_MODELS:
        table.add_row(model)
    console.print(table)

    table2 = Table(title="Available Embedding Models")
    table2.add_column("Model", style="bold cyan")
    for model in EMBEDDING_MODELS:
        table2.add_row(model)
    console.print(table2)

    table3 = Table(title="Available Image Models")
    table3.add_column("Model", style="bold cyan")
    for model in IMAGE_MODELS:
        table3.add_row(model)
    console.print(table3)

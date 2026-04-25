"""Rich terminal output formatting for OpenAI CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# ── Chat / Responses models ───────────────────────────────────────────────

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

DEFAULT_CHAT_MODEL = "gpt-4o-mini"

RESPONSES_MODELS = [
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

DEFAULT_RESPONSES_MODEL = "gpt-4o-mini"

# ── Embedding models ───────────────────────────────────────────────────────

EMBEDDING_MODELS = [
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
]

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

# ── Image models ───────────────────────────────────────────────────────────

IMAGE_MODELS = [
    "dall-e-3",
    "gpt-image-1",
    "gpt-image-1.5",
    "gpt-image-2",
    "nano-banana",
    "nano-banana-2",
    "nano-banana-pro",
]

DEFAULT_IMAGE_MODEL = "dall-e-3"

# ── Image sizes ────────────────────────────────────────────────────────────

IMAGE_SIZES = [
    "auto",
    "1024x1024",
    "1536x1024",
    "1024x1536",
]

# ── Image quality options ──────────────────────────────────────────────────

IMAGE_QUALITY = ["auto", "high", "medium", "low", "standard", "hd"]

# ── Image output formats ───────────────────────────────────────────────────

IMAGE_OUTPUT_FORMATS = ["png", "jpeg", "webp"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_chat_result(data: dict[str, Any]) -> None:
    """Print chat completion result."""
    choices = data.get("choices", [])
    model = data.get("model", "unknown")
    usage = data.get("usage", {})

    if not choices:
        console.print("[yellow]No response choices returned.[/yellow]")
        return

    for i, choice in enumerate(choices, 1):
        msg = choice.get("message", {})
        content = msg.get("content", "")
        role = msg.get("role", "assistant")
        finish_reason = choice.get("finish_reason", "")

        title = f"[bold green]Response[/bold green]"
        if len(choices) > 1:
            title = f"[bold green]Response #{i}[/bold green]"

        subtitle = f"[dim]{model}[/dim]"
        if finish_reason:
            subtitle += f" · finish: {finish_reason}"

        console.print(
            Panel(
                content or "[dim](empty)[/dim]",
                title=title,
                subtitle=subtitle,
                border_style="green",
            )
        )

    if usage:
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)
        console.print(
            f"\n[dim]Tokens: {prompt_tokens} prompt + {completion_tokens} completion"
            f" = {total_tokens} total[/dim]"
        )


def print_embed_result(data: dict[str, Any]) -> None:
    """Print embeddings result."""
    embeddings = data.get("data", [])
    model = data.get("model", "unknown")
    usage = data.get("usage", {})

    console.print(
        Panel(
            f"[bold]Model:[/bold] {model}\n"
            f"[bold]Embeddings:[/bold] {len(embeddings)}\n"
            f"[bold]Dimensions:[/bold] {len(embeddings[0].get('embedding', [])) if embeddings else 0}",
            title="[bold blue]Embeddings Result[/bold blue]",
            border_style="blue",
        )
    )

    if usage:
        total_tokens = usage.get("total_tokens", 0)
        console.print(f"\n[dim]Tokens used: {total_tokens}[/dim]")


def print_image_result(data: dict[str, Any]) -> None:
    """Print image generation/edit result."""
    task_id = data.get("task_id")
    trace_id = data.get("trace_id")
    images = data.get("data", [])

    info_lines = []
    if task_id:
        info_lines.append(f"[bold]Task ID:[/bold] {task_id}")
    if trace_id:
        info_lines.append(f"[bold]Trace ID:[/bold] {trace_id}")

    if info_lines:
        console.print(
            Panel(
                "\n".join(info_lines),
                title="[bold green]Image Result[/bold green]",
                border_style="green",
            )
        )

    if not images:
        console.print("[yellow]No image data available yet.[/yellow]")
        return

    for i, img in enumerate(images, 1):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan", width=15)
        table.add_column("Value")
        table.add_row("Image", f"#{i}")
        if img.get("url"):
            table.add_row("URL", img["url"])
        if img.get("b64_json"):
            table.add_row("Base64", "[dim](base64 data)[/dim]")
        if img.get("revised_prompt"):
            table.add_row("Revised Prompt", img["revised_prompt"][:80])
        console.print(table)
        console.print()


def print_models() -> None:
    """Print available OpenAI models."""
    table = Table(title="Available OpenAI Chat/Completion Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Type")

    for model in CHAT_MODELS:
        if model.startswith("gpt-5"):
            mtype = "GPT-5"
        elif model.startswith("gpt-4"):
            mtype = "GPT-4"
        elif model.startswith("o"):
            mtype = "Reasoning"
        else:
            mtype = "Other"
        table.add_row(model, mtype)

    console.print(table)
    console.print(f"\n[dim]Default chat model: {DEFAULT_CHAT_MODEL}[/dim]")

    table2 = Table(title="Available Embedding Models")
    table2.add_column("Model", style="bold cyan")
    for m in EMBEDDING_MODELS:
        table2.add_row(m)
    console.print(table2)
    console.print(f"\n[dim]Default embedding model: {DEFAULT_EMBEDDING_MODEL}[/dim]")

    table3 = Table(title="Available Image Models")
    table3.add_column("Model", style="bold cyan")
    for m in IMAGE_MODELS:
        table3.add_row(m)
    console.print(table3)
    console.print(f"\n[dim]Default image model: {DEFAULT_IMAGE_MODEL}[/dim]")

"""Rich terminal output formatting for AiChat CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Available models from OpenAPI spec
MODELS = [
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.6-sol",
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-5.4-nano",
    "gpt-5.4-pro",
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-5-all",
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
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v4-flash",
    "grok-4.5",
    "grok-3",
    "glm-5.2",
    "glm-5",
    "glm-5-turbo",
    "glm-5.1",
    "glm-4.7",
    "glm-4.6",
    "glm-3-turbo",
]

DEFAULT_MODEL = "gpt-4o"

# Available models for /aichat2/conversations endpoint
MODELS2 = [
    "gpt-4",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-5-all",
    "gpt-5.1-all",
    "gpt-5.2-pro",
    "gpt-5.4-mini",
    "gpt-5.4-nano",
    "gpt-image-1",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-7-sonnet-20250219",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-haiku-4-5-20251001",
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-opus-4-5-20251101",
    "claude-opus-4-6",
    "claude-fable-5",
    "claude-opus-4-8",
    "claude-opus-4-7",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-6",
    "claude-sonnet-5",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3-pro-preview",
    "gemini-3.1-flash-image-preview",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-pro",
    "gemini-3.1-pro-preview",
    "grok-3",
    "grok-3-fast",
    "grok-4",
    "grok-4.5",
    "grok-4-0709",
    "deepseek-chat",
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-reasoner",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v3.2-exp",
    "deepseek-v4-flash",
    "kimi-k2-0711-preview",
    "kimi-k2-0905-preview",
    "kimi-k2-instruct-0905",
    "kimi-k2-thinking",
    "kimi-k2-thinking-turbo",
    "kimi-k2-turbo-preview",
    "kimi-k3",
    "kimi-k2.6",
    "kimi-k2.5",
    "glm-3-turbo",
    "glm-4.5",
    "glm-4.5v",
    "glm-4.6",
    "glm-4.7",
    "glm-5",
    "glm-5-turbo",
    "glm-5.2",
    "glm-5.1",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
]

DEFAULT_MODEL2 = "gpt-4o"

# Available model groups for /aichat2/conversations endpoint
MODEL_GROUPS = ["chatgpt", "claude", "gemini", "grok", "kimi", "glm", "deepseek"]

# Available actions for /aichat2/conversations endpoint
ACTIONS2 = ["chat", "retrieve", "retrieve_batch", "update", "delete"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_answer(data: dict[str, Any]) -> None:
    """Print a conversation answer in a rich format."""
    answer = data.get("answer", "")
    conversation_id = data.get("id", "")

    if answer:
        console.print(
            Panel(
                answer,
                title="[bold blue]Answer[/bold blue]",
                border_style="blue",
            )
        )
    else:
        console.print("[yellow]No answer returned.[/yellow]")

    if conversation_id:
        console.print(f"\n[dim]Conversation ID: {conversation_id}[/dim]")


def print_models() -> None:
    """Print available models in a rich table."""
    table = Table(title="Available Models")
    table.add_column("Model", style="bold cyan")
    table.add_column("Family")

    for model in MODELS:
        table.add_row(model, _get_model_family(model))

    console.print(table)


def _get_model_family(model: str) -> str:
    """Get the model family for display purposes."""
    if model.startswith("gpt-5"):
        return "GPT-5"
    elif model.startswith("gpt-image"):
        return "GPT-Image"
    elif model.startswith("gpt-4.5"):
        return "GPT-4.5"
    elif model.startswith("gpt-4.1"):
        return "GPT-4.1"
    elif model.startswith("gpt-4o"):
        return "GPT-4o"
    elif model.startswith("gpt-4"):
        return "GPT-4"
    elif model.startswith("o1"):
        return "o1"
    elif model.startswith("o3-mini"):
        return "o3-mini"
    elif model.startswith("o3-pro"):
        return "o3-pro"
    elif model.startswith("o3"):
        return "o3"
    elif model.startswith("o4-mini"):
        return "o4-mini"
    elif model.startswith("claude"):
        return "Claude"
    elif model.startswith("gemini"):
        return "Gemini"
    elif model.startswith("grok"):
        return "Grok"
    elif model.startswith("deepseek"):
        return "DeepSeek"
    elif model.startswith("kimi"):
        return "Kimi"
    elif model.startswith("glm"):
        return "GLM"
    else:
        return "Other"


def print_models2() -> None:
    """Print available models for /aichat2/conversations in a rich table."""
    table = Table(title="Available Models (aichat2)")
    table.add_column("Model", style="bold cyan")
    table.add_column("Family")

    for model in MODELS2:
        table.add_row(model, _get_model_family(model))

    console.print(table)

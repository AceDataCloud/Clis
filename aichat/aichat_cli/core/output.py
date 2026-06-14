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
    "grok-3",
    "glm-5.1",
    "glm-4.7",
    "glm-4.6",
    "glm-3-turbo",
]

DEFAULT_MODEL = "gpt-4o"

# Available models for /aichat2/conversations endpoint (multi-provider)
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
    "claude-opus-4-7",
    "claude-opus-4-8",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-6",
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
    "kimi-k2.5",
    "glm-3-turbo",
    "glm-4.5",
    "glm-4.5v",
    "glm-4.6",
    "glm-4.7",
    "glm-5",
    "glm-5-turbo",
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
        if model.startswith("gpt-5"):
            family = "GPT-5"
        elif model.startswith("gpt-4.5"):
            family = "GPT-4.5"
        elif model.startswith("gpt-4.1"):
            family = "GPT-4.1"
        elif model.startswith("gpt-4o"):
            family = "GPT-4o"
        elif model.startswith("gpt-4"):
            family = "GPT-4"
        elif model.startswith("o1"):
            family = "o1"
        elif model.startswith("o3-mini"):
            family = "o3-mini"
        elif model.startswith("o3-pro"):
            family = "o3-pro"
        elif model.startswith("o3"):
            family = "o3"
        elif model.startswith("o4-mini"):
            family = "o4-mini"
        elif model.startswith("deepseek"):
            family = "DeepSeek"
        elif model.startswith("grok"):
            family = "Grok"
        elif model.startswith("glm"):
            family = "GLM"
        else:
            family = "Other"

        table.add_row(model, family)

    console.print(table)


def print_models2() -> None:
    """Print available models for the multi-provider aichat2 endpoint."""
    table = Table(title="Available Models (Multi-Provider)")
    table.add_column("Model", style="bold cyan")
    table.add_column("Provider")

    for model in MODELS2:
        if model.startswith("gpt") or model.startswith("o1") or model.startswith("o3") or model.startswith("o4"):
            provider = "OpenAI"
        elif model.startswith("claude"):
            provider = "Anthropic"
        elif model.startswith("gemini"):
            provider = "Google"
        elif model.startswith("grok"):
            provider = "xAI"
        elif model.startswith("deepseek"):
            provider = "DeepSeek"
        elif model.startswith("kimi"):
            provider = "Moonshot"
        elif model.startswith("glm"):
            provider = "Zhipu"
        else:
            provider = "Other"

        table.add_row(model, provider)

    console.print(table)
    console.print(f"\n[dim]Default model: {DEFAULT_MODEL2}[/dim]")

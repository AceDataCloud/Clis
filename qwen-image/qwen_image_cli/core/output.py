"""Console output for Qwen Image CLI."""

import json
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()
MODELS = ["qwen-image-3.0", "qwen-image-3.0-pro"]
DEFAULT_MODEL = "qwen-image-3.0"


def print_json(data: Any) -> None:
    console.print(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_image_result(data: dict[str, Any]) -> None:
    if data.get("task_id") and not data.get("data"):
        console.print(f"Task ID: {data['task_id']}")
        return
    for item in data.get("data", []):
        console.print(item.get("image_url", ""))


def print_models() -> None:
    table = Table(title="Qwen Image models")
    table.add_column("Model")
    table.add_column("Best for")
    table.add_row("qwen-image-3.0", "Value and throughput")
    table.add_row("qwen-image-3.0-pro", "Complex layouts and detail")
    console.print(table)


def print_success(message: str) -> None:
    console.print(f"[bold green]✓[/bold green] {message}")


def print_task_result(data: dict[str, Any]) -> None:
    print_json(data)

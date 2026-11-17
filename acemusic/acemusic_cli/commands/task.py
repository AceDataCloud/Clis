"""Authenticated free task queries and explicit file download."""

import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import click
import httpx

from acemusic_cli.core.client import get_client
from acemusic_cli.core.exceptions import AceMusicError
from acemusic_cli.core.output import print_json

TERMINAL = {
    "succeeded",
    "complete",
    "completed",
    "partial_failed",
    "failed",
    "error",
    "cancelled",
    "canceled",
}
FAILURE = {"partial_failed", "failed", "error", "cancelled", "canceled"}


def task_state(result: dict[str, Any]) -> str:
    state = str(result.get("state") or result.get("status") or "").lower()
    if state in TERMINAL:
        return state
    response = result.get("response") or {}
    if isinstance(response, dict):
        response_state = str(response.get("state") or response.get("status") or "").lower()
        if response_state in TERMINAL:
            return response_state
        if response.get("success") is False:
            return "failed"
        if response.get("success") is True and response.get("data"):
            return "succeeded"
    return state or "pending"


def query(ctx: click.Context, **payload: Any) -> dict[str, Any]:
    try:
        return get_client(ctx.obj.get("token")).query_task(**payload)
    except AceMusicError as error:
        raise click.ClickException(error.message) from error


@click.command()
@click.argument("task_id")
@click.option("--json", "output_json", is_flag=True)
@click.pass_context
def task(ctx: click.Context, task_id: str, output_json: bool) -> None:
    """Retrieve the original task without generating again."""
    del output_json
    print_json(query(ctx, action="retrieve", id=task_id))


@click.command("tasks")
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--json", "output_json", is_flag=True)
@click.pass_context
def tasks_batch(ctx: click.Context, task_ids: tuple[str, ...], output_json: bool) -> None:
    """Retrieve up to 50 original task IDs."""
    del output_json
    if len(task_ids) > 50:
        raise click.UsageError("At most 50 tasks per batch.")
    print_json(query(ctx, action="retrieve_batch", ids=list(task_ids)))


@click.command()
@click.option("--page", type=click.IntRange(min=1), default=1)
@click.option("--page-size", type=click.IntRange(1, 50), default=20)
@click.pass_context
def history(ctx: click.Context, page: int, page_size: int) -> None:
    """List your task history."""
    print_json(query(ctx, action="list", limit=page_size, offset=(page - 1) * page_size))


@click.command()
@click.argument("task_id")
@click.option("--interval", type=click.FloatRange(min=1), default=10, show_default=True)
@click.option(
    "--timeout", "max_timeout", type=click.FloatRange(min=1), default=600, show_default=True
)
@click.option("--json", "output_json", is_flag=True)
@click.pass_context
def wait(
    ctx: click.Context, task_id: str, interval: float, max_timeout: float, output_json: bool
) -> None:
    """Wait a bounded time for the SAME task; retain its ID after timeout."""
    del output_json
    deadline = time.monotonic() + max_timeout
    while True:
        result = query(ctx, action="retrieve", id=task_id)
        state = task_state(result)
        if state in TERMINAL:
            print_json(result)
            if state in FAILURE:
                raise click.exceptions.Exit(1)
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise click.ClickException(
                f"Still pending. Resume with: acemusic wait {task_id}. No replacement was submitted."
            )
        time.sleep(min(interval, remaining))


@click.command()
@click.argument("task_id")
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=Path("."),
    help="Destination directory; existing files are preserved.",
)
@click.pass_context
def download(ctx: click.Context, task_id: str, output: Path) -> None:
    """Download final successful MP3 candidates from your original task."""
    result = query(ctx, action="retrieve", id=task_id)
    state = task_state(result)
    if state not in TERMINAL:
        raise click.ClickException("Task is still processing. Wait using the original task ID.")
    response = result.get("response") or result
    items = response.get("data", []) if isinstance(response, dict) else []
    output.mkdir(parents=True, exist_ok=True)
    count = 0
    for index, item in enumerate(items, 1):
        url = item.get("audio_url") if isinstance(item, dict) else None
        if not url:
            continue
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != "cdn.acedata.cloud":
            raise click.ClickException("Expected a final Ace Data Cloud CDN audio URL.")
        target = output / f"{task_id}-{index}.mp3"
        with httpx.stream("GET", url, follow_redirects=False, timeout=120) as stream:
            stream.raise_for_status()
            with target.open("xb") as file:
                for chunk in stream.iter_bytes():
                    file.write(chunk)
        click.echo(str(target))
        count += 1
    if not count:
        raise click.ClickException("The terminal task contains no downloadable audio.")

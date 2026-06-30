"""Task management commands."""

import time

import click

from fish_cli.core.client import get_client
from fish_cli.core.exceptions import FishError
from fish_cli.core.output import (
    print_error,
    print_json,
    print_success,
    print_task_result,
    print_tasks_batch_result,
)


@click.command()
@click.argument("task_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def task(
    ctx: click.Context,
    task_id: str,
    output_json: bool,
) -> None:
    """Query a single task status.

    TASK_ID is the task ID returned from TTS generation commands.

    \\b
    Examples:
      fish task 2725a2d3-f87e-4905-9c53-9988d5a7b2f5
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("tasks")
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def tasks_batch(
    ctx: click.Context,
    task_ids: tuple[str, ...],
    output_json: bool,
) -> None:
    """Query multiple tasks at once.

    TASK_IDS are space-separated task IDs.

    \\b
    Examples:
      fish tasks abc123 def456 ghi789
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(ids=list(task_ids), action="retrieve_batch")
        if output_json:
            print_json(result)
        else:
            print_tasks_batch_result(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("task_id")
@click.option(
    "--interval",
    type=int,
    default=5,
    help="Polling interval in seconds (default: 5).",
)
@click.option(
    "--timeout",
    "max_timeout",
    type=int,
    default=600,
    help="Maximum wait time in seconds (default: 600).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def wait(
    ctx: click.Context,
    task_id: str,
    interval: int,
    max_timeout: int,
    output_json: bool,
) -> None:
    """Wait for a task to complete, polling periodically.

    TASK_ID is the task ID to monitor.

    \\b
    Examples:
      fish wait 2725a2d3-f87e-4905-9c53-9988d5a7b2f5

      fish wait 2725a2d3 --interval 10 --timeout 300
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    try:
        while elapsed < max_timeout:
            result = client.query_task(id=task_id, action="retrieve")
            response = result.get("response", {})
            data = response.get("data", []) if response else result.get("data", [])

            status = ""
            if isinstance(data, list) and data:
                status = data[0].get("status", "")
            elif isinstance(data, dict):
                status = data.get("status", "")

            # Check if we have an audio URL which means completion
            audio_url = None
            if isinstance(data, list) and data:
                audio_url = data[0].get("audio_url")
            elif isinstance(data, dict):
                audio_url = data.get("audio_url")

            if audio_url or status in (
                "done",
                "succeeded",
                "completed",
                "complete",
                "failed",
                "error",
            ):
                if output_json:
                    print_json(result)
                else:
                    if status in ("failed", "error"):
                        print_error(f"Task {task_id} failed.")
                    else:
                        print_success(f"Task {task_id} completed!")
                    print_task_result(result)
                return

            if not output_json:
                click.echo(f"Status: {status or 'pending'} (waited {elapsed}s)...", err=True)

            time.sleep(interval)
            elapsed += interval

        print_error(f"Timeout: task {task_id} did not complete within {max_timeout}s")
        raise SystemExit(1)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e

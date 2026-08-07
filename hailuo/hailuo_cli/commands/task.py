"""Task management commands."""

import time

import click

from hailuo_cli.core.client import get_client
from hailuo_cli.core.exceptions import HailuoError
from hailuo_cli.core.output import (
    print_error,
    print_json,
    print_success,
    print_task_result,
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

    TASK_ID is the task ID returned from generate commands.

    \b
    Examples:
      hailuo task abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except HailuoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("tasks")
@click.argument("task_ids", nargs=-1)
@click.option("--limit", type=int, help="Maximum number of tasks to return.")
@click.option("--offset", type=int, help="Number of tasks to skip.")
@click.option("--created-at-min", type=float, help="Minimum creation timestamp.")
@click.option("--created-at-max", type=float, help="Maximum creation timestamp.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def tasks_batch(
    ctx: click.Context,
    task_ids: tuple[str, ...],
    limit: int | None,
    offset: int | None,
    created_at_min: float | None,
    created_at_max: float | None,
    output_json: bool,
) -> None:
    """Query multiple tasks at once.

    TASK_IDS are space-separated task IDs.

    \b
    Examples:
      hailuo tasks abc123 def456 ghi789
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(
            ids=list(task_ids) or None,
            action="retrieve_batch",
            limit=limit,
            offset=offset,
            created_at_min=created_at_min,
            created_at_max=created_at_max,
        )
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except HailuoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("task_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def delete(ctx: click.Context, task_id: str, output_json: bool) -> None:
    """Delete a task.

    TASK_ID is the task ID to delete.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id, action="delete")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except HailuoError as e:
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

    \b
    Examples:
      hailuo wait abc123
      hailuo wait abc123 --interval 10 --timeout 300
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    try:
        while elapsed < max_timeout:
            result = client.query_task(id=task_id, action="retrieve")

            item = result.get("task", result)
            state = item.get("status", "")
            content = item.get("content")
            video_url = content.get("url") if isinstance(content, dict) else None
            error = item.get("error")

            if error:
                if output_json:
                    print_json(result)
                else:
                    print_error(f"Task {task_id} failed: {error}")
                raise SystemExit(1)

            if state == "succeeded" or video_url:
                if output_json:
                    print_json(result)
                else:
                    print_success(f"Task {task_id} completed!")
                    print_task_result(result)
                return

            if state in ("failed", "cancelled"):
                if output_json:
                    print_json(result)
                else:
                    print_error(f"Task {task_id} failed.")
                raise SystemExit(1)

            if not output_json:
                click.echo(f"Status: {state or 'pending'} (waited {elapsed}s)...", err=True)

            time.sleep(interval)
            elapsed += interval

        print_error(f"Timeout: task {task_id} did not complete within {max_timeout}s")
        raise SystemExit(1)
    except HailuoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

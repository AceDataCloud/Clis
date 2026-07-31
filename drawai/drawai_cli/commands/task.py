"""Task management commands for DrawAI CLI."""

import time

import click

from drawai_cli.core.client import get_client
from drawai_cli.core.exceptions import DrawAIError
from drawai_cli.core.output import print_error, print_json, print_success, print_task_result


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
      drawai task abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except DrawAIError as e:
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

    \b
    Examples:
      drawai tasks abc123 def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(ids=list(task_ids), action="retrieve_batch")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except DrawAIError as e:
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
    default=300,
    help="Maximum wait time in seconds (default: 300).",
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
      drawai wait abc123
      drawai wait abc123 --interval 10 --timeout 120
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    try:
        while elapsed < max_timeout:
            result = client.query_task(id=task_id, action="retrieve")
            state = result.get("state", "")

            if state in ("succeed", "succeeded", "completed", "complete", "done", "failed", "error"):
                if output_json:
                    print_json(result)
                else:
                    if state in ("failed", "error"):
                        print_error(f"Task {task_id} failed.")
                    else:
                        print_success(f"Task {task_id} completed!")
                    print_task_result(result)
                return

            if not output_json:
                click.echo(f"State: {state or 'pending'} (waited {elapsed}s)...", err=True)

            time.sleep(interval)
            elapsed += interval

        print_error(f"Timeout: task {task_id} did not complete within {max_timeout}s")
        raise SystemExit(1)
    except DrawAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

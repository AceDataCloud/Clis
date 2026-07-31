"""Task management commands for Digital Human CLI."""

import time

import click

from digitalhuman_cli.core.client import get_client
from digitalhuman_cli.core.exceptions import DigitalHumanError
from digitalhuman_cli.core.output import print_error, print_json, print_success, print_task_result


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
      digitalhuman task task_49af42c410c24f04ad416b28af55d237
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(task_id=task_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except DigitalHumanError as e:
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
      digitalhuman tasks task_abc123 task_def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(
            task_id=task_ids[0] if len(task_ids) == 1 else None,
            action="retrieve_batch",
        )
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except DigitalHumanError as e:
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
      digitalhuman wait task_49af42c410c24f04ad416b28af55d237
      digitalhuman wait task_abc123 --interval 10 --timeout 300
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    try:
        while elapsed < max_timeout:
            result = client.query_task(task_id=task_id)
            state = result.get("state", "")

            if state in ("succeed", "succeeded", "completed", "complete", "failed", "error"):
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
    except DigitalHumanError as e:
        print_error(e.message)
        raise SystemExit(1) from e

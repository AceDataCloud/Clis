"""Task management commands."""

import time

import click

from dreamina_cli.core.client import get_client
from dreamina_cli.core.exceptions import DreaminaError
from dreamina_cli.core.output import print_error, print_json, print_success, print_task_result


@click.command()
@click.argument("task_id", required=False)
@click.option(
    "--trace-id",
    default=None,
    help="Trace ID to query when task ID is not available.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def task(
    ctx: click.Context,
    task_id: str | None,
    trace_id: str | None,
    output_json: bool,
) -> None:
    """Query a single task status.

    TASK_ID is the task ID returned from generate commands.

    \b
    Examples:
      dreamina task abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        if not task_id and not trace_id:
            raise click.UsageError("Provide either a task ID or use --trace-id.")

        result = client.query_task(id=task_id, trace_id=trace_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except DreaminaError as e:
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
      dreamina tasks abc123 def456 ghi789
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(ids=list(task_ids), action="retrieve_batch")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except DreaminaError as e:
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
      dreamina wait abc123

      dreamina wait abc123 --interval 10 --timeout 300
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    try:
        while elapsed < max_timeout:
            result = client.query_task(id=task_id, action="retrieve")
            response = result.get("response", {})
            data = response.get("data", {}) if response else result.get("data", {})

            status = ""
            if isinstance(data, dict):
                status = data.get("status", "")
            elif isinstance(data, list) and data:
                status = data[0].get("status", "")

            if status in ("done", "succeeded", "completed", "complete", "failed", "error"):
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
    except DreaminaError as e:
        print_error(e.message)
        raise SystemExit(1) from e

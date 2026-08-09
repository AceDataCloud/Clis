"""Task management commands."""

import time

import click

from veo_cli.core.client import get_client
from veo_cli.core.exceptions import VeoError
from veo_cli.core.output import print_error, print_json, print_success, print_task_result


@click.command()
@click.argument("task_id", required=False)
@click.option("--trace-id", default=None, help="Trace ID alternative to task ID.")
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

    Examples:

      veo task abc123-def456
      veo task --trace-id trace-123
    """
    if not task_id and not trace_id:
        raise click.UsageError("Provide TASK_ID or --trace-id.")

    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id, trace_id=trace_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("tasks")
@click.argument("task_ids", nargs=-1, required=False)
@click.option("--trace-ids", multiple=True, help="Trace IDs to retrieve (repeatable).")
@click.option("--offset", default=None, type=int, help="Pagination offset (default 0).")
@click.option("--limit", default=None, type=int, help="Page size (default 12).")
@click.option("--type", "task_type", default=None, help="Optional task type filter.")
@click.option("--created-at-min", default=None, type=float, help="Start timestamp (Unix seconds).")
@click.option("--created-at-max", default=None, type=float, help="End timestamp (Unix seconds).")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def tasks_batch(
    ctx: click.Context,
    task_ids: tuple[str, ...],
    trace_ids: tuple[str, ...],
    offset: int | None,
    limit: int | None,
    task_type: str | None,
    created_at_min: float | None,
    created_at_max: float | None,
    output_json: bool,
) -> None:
    """Query multiple tasks at once.

    TASK_IDS are space-separated task IDs.

    Examples:

      veo tasks abc123 def456 ghi789
      veo tasks --trace-ids trace-123 --trace-ids trace-456
      veo tasks --offset 0 --limit 20
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(
            ids=list(task_ids) if task_ids else None,
            trace_ids=list(trace_ids) if trace_ids else None,
            offset=offset,
            limit=limit,
            type=task_type,
            created_at_min=created_at_min,
            created_at_max=created_at_max,
            action="retrieve_batch",
        )
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("task_id", required=False)
@click.option("--trace-id", default=None, help="Trace ID alternative to task ID.")
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
    task_id: str | None,
    trace_id: str | None,
    interval: int,
    max_timeout: int,
    output_json: bool,
) -> None:
    """Wait for a task to complete, polling periodically.

    TASK_ID is the task ID to monitor.

    Examples:

      veo wait abc123
      veo wait --trace-id trace-123

      veo wait abc123 --interval 10 --timeout 300
    """
    if not task_id and not trace_id:
        raise click.UsageError("Provide TASK_ID or --trace-id.")

    client = get_client(ctx.obj.get("token"))
    elapsed = 0
    task_label = trace_id or task_id or "task"

    try:
        while elapsed < max_timeout:
            result = client.query_task(id=task_id, trace_id=trace_id, action="retrieve")
            data = result.get("data", result)

            # Check completion - handle both list and dict responses
            if isinstance(data, list) and data:
                item = data[0]
            elif isinstance(data, dict):
                item = data
            else:
                item = result if result.get("id") or result.get("state") else {}

            state = item.get("state", item.get("status", ""))
            if state in ("succeeded", "completed", "complete", "failed", "error"):
                if output_json:
                    print_json(result)
                else:
                    if state in ("failed", "error"):
                        print_error(f"Task {task_label} failed.")
                    else:
                        print_success(f"Task {task_label} completed!")
                    print_task_result(result)
                return

            if not output_json:
                click.echo(f"Status: {state or 'pending'} (waited {elapsed}s)...", err=True)

            time.sleep(interval)
            elapsed += interval

        print_error(f"Timeout: task {task_label} did not complete within {max_timeout}s")
        raise SystemExit(1)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

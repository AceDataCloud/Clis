"""Tasks API commands for querying async render/extract task results."""

import click

from webextrator_cli.core.client import get_client
from webextrator_cli.core.exceptions import WebExtraterError
from webextrator_cli.core.output import (
    print_error,
    print_json,
    print_task_batch_result,
    print_task_result,
)


@click.group()
def tasks() -> None:
    """Query WebExtrator async task results (`/webextrator/tasks`).

    Use these commands to retrieve results of render or extract tasks
    that were submitted with a callback_url.

    \b
    Examples:
      webextrator tasks retrieve --id 550e8400-e29b-41d4-a716-446655440000
      webextrator tasks retrieve --trace-id my-custom-trace-001
      webextrator tasks batch --ids id1 id2
    """


@tasks.command()
@click.option("--id", "task_id", default=None, help="Task ID returned when the job was submitted.")
@click.option("--trace-id", default=None, help="Trace ID associated with the task.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def retrieve(
    ctx: click.Context,
    task_id: str | None,
    trace_id: str | None,
    output_json: bool,
) -> None:
    """Retrieve a single task by ID or trace ID.

    Either --id or --trace-id must be provided.

    \b
    Examples:
      webextrator tasks retrieve --id 550e8400-e29b-41d4-a716-446655440000
      webextrator tasks retrieve --trace-id my-custom-trace-001
    """
    if not task_id and not trace_id:
        raise click.UsageError("Provide at least one of --id or --trace-id.")

    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "retrieve",
        "id": task_id,
        "trace_id": trace_id,
    }

    try:
        result = client.tasks(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except WebExtraterError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@tasks.command()
@click.option("--ids", multiple=True, help="Task IDs to retrieve (repeatable).")
@click.option("--trace-ids", multiple=True, help="Trace IDs to retrieve (repeatable).")
@click.option("--offset", default=None, type=int, help="Pagination offset (default 0).")
@click.option("--limit", default=None, type=int, help="Page size (default 12).")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def batch(
    ctx: click.Context,
    ids: tuple[str, ...],
    trace_ids: tuple[str, ...],
    offset: int | None,
    limit: int | None,
    output_json: bool,
) -> None:
    """Retrieve multiple tasks at once.

    Filter by IDs or trace IDs.

    \b
    Examples:
      webextrator tasks batch --ids id1 id2
      webextrator tasks batch --trace-ids trace-001 trace-002
      webextrator tasks batch --ids id1 --limit 5
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "retrieve_batch",
        "ids": list(ids) if ids else None,
        "trace_ids": list(trace_ids) if trace_ids else None,
        "offset": offset,
        "limit": limit,
    }

    try:
        result = client.tasks(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_task_batch_result(result)
    except WebExtraterError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Task management commands for WebExtrator."""

import click

from webextrator_cli.core.client import get_client
from webextrator_cli.core.exceptions import WebExtratorError
from webextrator_cli.core.output import print_error, print_json, print_task_result


@click.group()
def tasks() -> None:
    """Query previously created render/extract tasks.

    \b
    Examples:
      webextrator tasks retrieve --id 550e8400-e29b-41d4-a716-446655440000
      webextrator tasks retrieve --trace-id 550e8400-e29b-41d4-a716-446655440001
      webextrator tasks batch --ids id1 id2
    """


@tasks.command()
@click.option("--id", "task_id", default=None, help="Task UUID to retrieve.")
@click.option("--trace-id", default=None, help="Trace UUID to retrieve.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def retrieve(
    ctx: click.Context,
    task_id: str | None,
    trace_id: str | None,
    output_json: bool,
) -> None:
    """Retrieve a single render/extract task by ID or trace ID.

    \b
    Examples:
      webextrator tasks retrieve --id 550e8400-e29b-41d4-a716-446655440000
      webextrator tasks retrieve --trace-id 550e8400-e29b-41d4-a716-446655440001
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
    except WebExtratorError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@tasks.command()
@click.option("--ids", multiple=True, help="Task UUIDs to retrieve (repeatable).")
@click.option("--trace-ids", multiple=True, help="Trace UUIDs to retrieve (repeatable).")
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
    """Retrieve multiple render/extract tasks at once.

    \b
    Examples:
      webextrator tasks batch --ids id1 id2
      webextrator tasks batch --trace-ids trace-001 trace-002
      webextrator tasks batch --limit 5
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
            print_task_result(result)
    except WebExtratorError as e:
        print_error(e.message)
        raise SystemExit(1) from e

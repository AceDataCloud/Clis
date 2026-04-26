"""Tasks API commands for querying async image task results."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    print_error,
    print_json,
    print_task_batch_result,
    print_task_result,
)


@click.group()
def tasks() -> None:
    """Query OpenAI async task results (`/openai/tasks`).

    Use these commands to retrieve results of image generation or editing
    tasks that were submitted with a callback_url.

    \b
    Examples:
      openai-cli tasks retrieve --id 7489df4c-ef03-4de0-b598-e9a590793434
      openai-cli tasks retrieve --trace-id my-custom-trace-001
      openai-cli tasks batch --trace-ids trace-001 trace-002
      openai-cli tasks batch --application-id 9dec7b2a-1cad-41ff-8536-d4ddaf2525d4
    """


@tasks.command()
@click.option("--id", "task_id", default=None, help="Task ID returned when the job was submitted.")
@click.option("--trace-id", default=None, help="Custom trace ID passed in the original request.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def retrieve(
    ctx: click.Context,
    task_id: str | None,
    trace_id: str | None,
    output_json: bool,
) -> None:
    """Retrieve a single task by ID or trace ID.

    Either --id or --trace-id must be provided. When both are given,
    --trace-id takes precedence.

    \b
    Examples:
      openai-cli tasks retrieve --id 7489df4c-ef03-4de0-b598-e9a590793434
      openai-cli tasks retrieve --trace-id my-custom-trace-001
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
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@tasks.command()
@click.option("--ids", multiple=True, help="Task IDs to retrieve (repeatable).")
@click.option("--trace-ids", multiple=True, help="Trace IDs to retrieve (repeatable).")
@click.option("--application-id", default=None, help="Filter by application ID.")
@click.option("--user-id", default=None, help="Filter by end-user ID.")
@click.option("--type", "task_type", default=None, help="Filter by task type (e.g. images_generations).")
@click.option("--offset", default=None, type=int, help="Pagination offset (default 0).")
@click.option("--limit", default=None, type=int, help="Page size (default 12).")
@click.option("--created-at-min", default=None, type=float, help="Start timestamp (Unix seconds).")
@click.option("--created-at-max", default=None, type=float, help="End timestamp (Unix seconds).")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def batch(
    ctx: click.Context,
    ids: tuple[str, ...],
    trace_ids: tuple[str, ...],
    application_id: str | None,
    user_id: str | None,
    task_type: str | None,
    offset: int | None,
    limit: int | None,
    created_at_min: float | None,
    created_at_max: float | None,
    output_json: bool,
) -> None:
    """Retrieve multiple tasks at once.

    Filter by IDs, trace IDs, application, user, or a creation time window.

    \b
    Examples:
      openai-cli tasks batch --trace-ids trace-001 trace-002
      openai-cli tasks batch --application-id 9dec7b2a-1cad-41ff-8536-d4ddaf2525d4
      openai-cli tasks batch --ids id1 id2 --limit 5
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "retrieve_batch",
        "ids": list(ids) if ids else None,
        "trace_ids": list(trace_ids) if trace_ids else None,
        "application_id": application_id,
        "user_id": user_id,
        "type": task_type,
        "offset": offset,
        "limit": limit,
        "created_at_min": created_at_min,
        "created_at_max": created_at_max,
    }

    try:
        result = client.tasks(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_task_batch_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Task retrieval commands for async image jobs."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import print_error, print_json, print_task_result


@click.command()
@click.option(
    "--id",
    "task_id",
    default=None,
    help="Task ID returned from an async image request.",
)
@click.option(
    "--trace-id",
    default=None,
    help="Custom trace ID passed in the original request.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def task(
    ctx: click.Context,
    task_id: str | None,
    trace_id: str | None,
    output_json: bool,
) -> None:
    """Retrieve a single async image task by ID or trace ID.

    Async tasks are created when an image request is submitted with a
    --callback-url.  Pass either --id or --trace-id (or both).

    \b
    Examples:
      openai-cli task --id 7489df4c-ef03-4de0-b598-e9a590793434
      openai-cli task --trace-id my-custom-trace-001
    """
    if not task_id and not trace_id:
        raise click.UsageError("Provide at least one of --id or --trace-id.")
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {"action": "retrieve"}
    if task_id:
        payload["id"] = task_id
    if trace_id:
        payload["trace_id"] = trace_id
    try:
        result = client.query_tasks(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("tasks")
@click.option(
    "--ids",
    multiple=True,
    help="Task IDs to query (repeatable).",
)
@click.option(
    "--trace-ids",
    multiple=True,
    help="Custom trace IDs to query (repeatable).",
)
@click.option(
    "--application-id",
    default=None,
    help="Filter tasks by application ID.",
)
@click.option(
    "--user-id",
    default=None,
    help="Filter tasks by user ID.",
)
@click.option(
    "--type",
    "task_type",
    default=None,
    help="Filter by task type (e.g. images_generations).",
)
@click.option(
    "--offset",
    default=None,
    type=int,
    help="Pagination offset (default: 0).",
)
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Maximum number of results to return (default: 12).",
)
@click.option(
    "--created-at-min",
    default=None,
    type=float,
    help="Filter tasks created after this Unix timestamp.",
)
@click.option(
    "--created-at-max",
    default=None,
    type=float,
    help="Filter tasks created before this Unix timestamp.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def tasks(
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
    """Retrieve multiple async image tasks at once.

    Filter by task IDs, trace IDs, application, user, or time window.

    \b
    Examples:
      openai-cli tasks --ids abc123 --ids def456
      openai-cli tasks --trace-ids my-trace-001 --trace-ids my-trace-002
      openai-cli tasks --application-id 9dec7b2a-... --limit 20
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {"action": "retrieve_batch"}
    if ids:
        payload["ids"] = list(ids)
    if trace_ids:
        payload["trace_ids"] = list(trace_ids)
    if application_id:
        payload["application_id"] = application_id
    if user_id:
        payload["user_id"] = user_id
    if task_type:
        payload["type"] = task_type
    if offset is not None:
        payload["offset"] = offset
    if limit is not None:
        payload["limit"] = limit
    if created_at_min is not None:
        payload["created_at_min"] = created_at_min
    if created_at_max is not None:
        payload["created_at_max"] = created_at_max
    try:
        result = client.query_tasks(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

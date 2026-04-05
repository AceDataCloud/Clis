"""Task management commands."""

import time

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import (
    print_error,
    print_json,
    print_seed_result,
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

    TASK_ID is the task ID returned from generate/imagine commands.

    \b
    Examples:
      midjourney task abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except MidjourneyError as e:
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
      midjourney tasks abc123 def456 ghi789
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(ids=list(task_ids), action="retrieve_batch")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except MidjourneyError as e:
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
      midjourney wait abc123
      midjourney wait abc123 --interval 10 --timeout 300
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    try:
        while elapsed < max_timeout:
            result = client.query_task(id=task_id, action="retrieve")

            # Check for completion signals
            success = result.get("success")
            image_url = result.get("image_url")
            video_urls = result.get("video_urls")
            error = result.get("error")

            if error:
                if output_json:
                    print_json(result)
                else:
                    print_error(f"Task {task_id} failed: {error}")
                raise SystemExit(1)

            if success and (image_url or video_urls):
                if output_json:
                    print_json(result)
                else:
                    print_success(f"Task {task_id} completed!")
                    print_task_result(result)
                return

            if not output_json:
                click.echo(f"Status: pending (waited {elapsed}s)...", err=True)

            time.sleep(interval)
            elapsed += interval

        print_error(f"Timeout: task {task_id} did not complete within {max_timeout}s")
        raise SystemExit(1)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("image_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def seed(
    ctx: click.Context,
    image_id: str,
    output_json: bool,
) -> None:
    """Get the seed value of a generated image.

    IMAGE_ID is the image_id from a previous generation.
    Use the seed with --seed in prompts for reproducible results.

    \b
    Examples:
      midjourney seed abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_seed(image_id=image_id)
        if output_json:
            print_json(result)
        else:
            print_seed_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

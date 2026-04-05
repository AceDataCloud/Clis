"""Task management commands."""

import time

import click

from adc_cli.core.client import get_client
from adc_cli.core.exceptions import AdcError
from adc_cli.core.output import print_error, print_json, print_success, print_task_result


@click.command()
@click.argument("task_id")
@click.option(
    "-s",
    "--service",
    type=click.Choice(
        ["flux", "midjourney", "suno", "luma", "sora", "veo", "seedance", "seedream", "nanobanana"]
    ),
    default="flux",
    help="Service the task belongs to.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def task(
    ctx: click.Context,
    task_id: str,
    service: str,
    output_json: bool,
) -> None:
    """Query a task status.

    TASK_ID is the task ID from a generate command.

    \b
    Examples:
      adc task abc123 -s flux
      adc task def456 -s luma
      adc task ghi789 -s suno --json
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(service, id=task_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("wait")
@click.argument("task_id")
@click.option(
    "-s",
    "--service",
    type=click.Choice(
        ["flux", "midjourney", "suno", "luma", "sora", "veo", "seedance", "seedream", "nanobanana"]
    ),
    default="flux",
    help="Service the task belongs to.",
)
@click.option("--interval", type=int, default=5, help="Polling interval in seconds.")
@click.option("--timeout", "max_timeout", type=int, default=600, help="Max wait time in seconds.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def wait_task(
    ctx: click.Context,
    task_id: str,
    service: str,
    interval: int,
    max_timeout: int,
    output_json: bool,
) -> None:
    """Wait for a task to complete.

    TASK_ID is the task ID to monitor.

    \b
    Examples:
      adc wait abc123 -s flux
      adc wait def456 -s luma --interval 10
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    try:
        while elapsed < max_timeout:
            result = client.query_task(service, id=task_id, action="retrieve")
            data = result.get("data", {})

            if isinstance(data, list) and data:
                item = data[0]
            elif isinstance(data, dict):
                item = data
            else:
                item = {}

            state = item.get("state", item.get("status", ""))
            if state in ("succeeded", "completed", "complete", "failed", "error"):
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
                click.echo(f"Status: {state or 'pending'} (waited {elapsed}s)...", err=True)

            time.sleep(interval)
            elapsed += interval

        print_error(f"Timeout: task {task_id} did not complete within {max_timeout}s")
        raise SystemExit(1)
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e

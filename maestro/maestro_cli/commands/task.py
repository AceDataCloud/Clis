"""Task management commands."""

import time

import click

from maestro_cli.core.client import get_client
from maestro_cli.core.exceptions import MaestroError
from maestro_cli.core.output import print_error, print_json, print_success, print_task_result


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

    TASK_ID is the task ID returned from the create command.

    Examples:

      maestro task abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id, action="retrieve")
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except MaestroError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("task_id")
@click.option(
    "--interval",
    type=int,
    default=10,
    help="Polling interval in seconds (default: 10).",
)
@click.option(
    "--timeout",
    "max_timeout",
    type=int,
    default=1800,
    help="Maximum wait time in seconds (default: 1800).",
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

    Examples:

      maestro wait abc123

      maestro wait abc123 --interval 15 --timeout 3600
    """
    client = get_client(ctx.obj.get("token"))
    elapsed = 0

    terminal_states = ("succeeded", "failed")

    try:
        while elapsed < max_timeout:
            result = client.query_task(id=task_id, action="retrieve")
            status = result.get("status", "")

            if status in terminal_states:
                if output_json:
                    print_json(result)
                else:
                    if status == "failed":
                        print_error(f"Task {task_id} failed.")
                    else:
                        print_success(f"Task {task_id} completed!")
                    print_task_result(result)
                if status == "failed":
                    raise SystemExit(1)
                return

            if not output_json:
                click.echo(f"Status: {status or 'pending'} (waited {elapsed}s)...", err=True)

            time.sleep(interval)
            elapsed += interval

        print_error(f"Timeout: task {task_id} did not complete within {max_timeout}s")
        raise SystemExit(1)
    except MaestroError as e:
        print_error(e.message)
        raise SystemExit(1) from e

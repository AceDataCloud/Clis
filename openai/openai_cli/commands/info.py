"""Info and utility commands."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.config import settings
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import console, print_api_models, print_error, print_json


@click.command()
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def models(ctx: click.Context, output_json: bool) -> None:
    """List available models from the OpenAI models endpoint."""
    client = get_client(ctx.obj.get("token"))

    try:
        result = client.models()
        if output_json:
            print_json(result)
        else:
            print_api_models(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    table = Table(title="OpenAI CLI Configuration")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}..." if settings.api_token else "[red]Not set[/red]",
    )
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)

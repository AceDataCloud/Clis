"""Maestro CLI entry point."""

import click

from maestro_cli.commands.info import config, models
from maestro_cli.commands.task import task, wait
from maestro_cli.commands.video import create
from maestro_cli.core.config import settings


@click.group()
@click.option("--token", envvar="ACEDATA_API_TOKEN", default=None, help="AceData API token.")
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Maestro AI video generation CLI."""
    ctx.ensure_object(dict)
    ctx.obj["token"] = token or settings.api_token


cli.add_command(create)
cli.add_command(task)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)

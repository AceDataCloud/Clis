#!/usr/bin/env python3
"""
Grok CLI - AI Chat and Video Generation via AceDataCloud API.

A command-line tool for Grok chat completions and video generation
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from grok_cli.commands.chat import chat
from grok_cli.commands.info import config, models
from grok_cli.commands.task import task, tasks_batch, wait
from grok_cli.commands.video import video

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("grok-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="grok-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Grok CLI - AI Chat and Video Generation powered by AceDataCloud.

    Chat with Grok models and generate videos from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      grok chat "What is the capital of France?"
      grok video "A sunset over the ocean"
      grok task abc123-def456
      grok wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(video)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

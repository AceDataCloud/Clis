#!/usr/bin/env python3
"""
DrawAI CLI - AI ID Photo Generation via AceDataCloud API.

A command-line tool for generating AI headshots and ID photos using
the AceDataCloud DrawAI service.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from drawai_cli.commands.headshot import generate
from drawai_cli.commands.info import config, templates
from drawai_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("drawai-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="drawai-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """DrawAI CLI - AI ID Photo Generation powered by AceDataCloud.

    Generate professional AI headshots and ID photos from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      drawai generate --image-url https://example.com/face.jpg
      drawai generate --image-url https://example.com/face.jpg --template wedding
      drawai task abc123-def456
      drawai wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(templates)
cli.add_command(config)


if __name__ == "__main__":
    cli()

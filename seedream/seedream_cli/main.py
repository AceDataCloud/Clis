#!/usr/bin/env python3
"""
Seedream CLI - AI Seedream Image Generation via AceDataCloud API.

A command-line tool for generating AI images using Seedream
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from seedream_cli.commands.image import edit, generate
from seedream_cli.commands.info import config, models, resolutions
from seedream_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("seedream-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="seedream-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Seedream CLI - AI Image Generation powered by AceDataCloud.

    Generate AI images from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      seedream generate "A beautiful landscape painting"
      seedream edit "Make it look like a painting" -i photo.jpg
      seedream task abc123-def456
      seedream wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(edit)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)
cli.add_command(resolutions)


if __name__ == "__main__":
    cli()

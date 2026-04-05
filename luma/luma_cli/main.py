#!/usr/bin/env python3
"""
Luma CLI - AI Luma Video Generation via AceDataCloud API.

A command-line tool for generating AI videos using Luma
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from luma_cli.commands.info import aspect_ratios, config, models
from luma_cli.commands.task import task, tasks_batch, wait
from luma_cli.commands.video import extend, generate, image_to_video

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("luma-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="luma-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Luma CLI - AI Video Generation powered by AceDataCloud.

    Generate AI videos from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      luma generate "A cinematic scene of a sunset over the ocean"
      luma task abc123-def456
      luma wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(image_to_video)
cli.add_command(extend)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(config)
cli.add_command(aspect_ratios)
cli.add_command(models)


if __name__ == "__main__":
    cli()

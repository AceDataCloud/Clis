#!/usr/bin/env python3
"""
AceDataCloud CLI - Unified CLI for AI services.

A single entry point for generating images, videos, music,
and searching the web using AceDataCloud's AI platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from adc_cli.commands.auth import auth
from adc_cli.commands.image import image
from adc_cli.commands.info import config, services
from adc_cli.commands.music import music
from adc_cli.commands.search import search
from adc_cli.commands.task import task, wait_task
from adc_cli.commands.video import video

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("acedatacloud-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="adc")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """AceDataCloud CLI - AI services from the command line.

    Generate images, videos, music, and search the web.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      adc auth login                              # Save your token
      adc image "A sunset over mountains"          # Generate an image
      adc video "A cinematic ocean scene"          # Generate a video
      adc music "Upbeat electronic dance track"    # Generate music
      adc search "artificial intelligence"         # Search Google

    \b
    Check results:
      adc task abc123 -s flux                      # Check task status
      adc wait abc123 -s flux                      # Wait for completion

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(auth)
cli.add_command(image)
cli.add_command(video)
cli.add_command(music)
cli.add_command(search)
cli.add_command(task)
cli.add_command(wait_task)
cli.add_command(services)
cli.add_command(config)


if __name__ == "__main__":
    cli()

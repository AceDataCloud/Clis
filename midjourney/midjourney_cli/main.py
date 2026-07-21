#!/usr/bin/env python3
"""
Midjourney CLI - AI Midjourney Image/Video Generation via AceDataCloud API.

A command-line tool for generating AI images and videos using Midjourney
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from midjourney_cli.commands.edits import edits
from midjourney_cli.commands.imagine import imagine
from midjourney_cli.commands.info import config
from midjourney_cli.commands.task import task, tasks_batch, wait
from midjourney_cli.commands.utility import describe, seed, shorten, translate
from midjourney_cli.commands.videos import videos

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("midjourney-pro-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="midjourney-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Midjourney CLI - AI Image/Video Generation powered by AceDataCloud.

    Generate AI images and videos from the command line using Midjourney.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      midjourney imagine "A beautiful sunset over the ocean"
      midjourney edits --image-url https://example.com/photo.jpg --prompt "Add mountains"
      midjourney videos --prompt "A flowing river" --action generate
      midjourney describe --image-url https://example.com/photo.jpg
      midjourney shorten "A very long and detailed prompt"
      midjourney translate "Una hermosa puesta de sol"
      midjourney seed --image-id abc123
      midjourney task abc123-def456
      midjourney wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(imagine)
cli.add_command(edits)
cli.add_command(videos)
cli.add_command(describe)
cli.add_command(shorten)
cli.add_command(translate)
cli.add_command(seed)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(config)


if __name__ == "__main__":
    cli()

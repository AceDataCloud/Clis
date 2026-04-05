#!/usr/bin/env python3
"""
Midjourney CLI - AI Image & Video Generation via AceDataCloud API.

A command-line tool for generating AI images and videos using Midjourney
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from midjourney_cli.commands.edit import describe, edit, translate
from midjourney_cli.commands.imagine import blend, imagine, transform
from midjourney_cli.commands.info import actions, config, modes, versions
from midjourney_cli.commands.task import seed, task, tasks_batch, wait
from midjourney_cli.commands.video import extend_video, video

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
    """Midjourney CLI - AI Image & Video Generation powered by AceDataCloud.

    Generate AI images and videos from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      midjourney imagine "A majestic lion at sunset"
      midjourney transform abc123 upscale1
      midjourney edit https://example.com/img.jpg "Make it a painting"
      midjourney video "A cat walking" --image-url https://example.com/cat.jpg
      midjourney task abc123-def456
      midjourney wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Image generation
cli.add_command(imagine)
cli.add_command(transform)
cli.add_command(blend)

# Image editing & description
cli.add_command(edit)
cli.add_command(describe)
cli.add_command(translate)

# Video
cli.add_command(video)
cli.add_command(extend_video)

# Task management
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(seed)

# Info
cli.add_command(config)
cli.add_command(modes)
cli.add_command(versions)
cli.add_command(actions)


if __name__ == "__main__":
    cli()

#!/usr/bin/env python3
"""
Kling CLI - AI Kling Video Generation via AceDataCloud API.

A command-line tool for generating AI videos using Kling
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from kling_cli.commands.info import aspect_ratios, config, models
from kling_cli.commands.motion import motion
from kling_cli.commands.task import task, tasks_batch, wait
from kling_cli.commands.video import extend, generate, image_to_video

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("kling-pro-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="kling-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Kling CLI - AI Video Generation powered by AceDataCloud.

    Generate AI videos from the command line using Kling models.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      kling generate "A cinematic scene of a sunset over the ocean"
      kling image-to-video "Animate this" --start-image-url https://example.com/photo.jpg
      kling motion --image-url img.jpg --video-url ref.mp4
      kling task abc123-def456
      kling wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(image_to_video)
cli.add_command(extend)
cli.add_command(motion)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(aspect_ratios)
cli.add_command(config)


if __name__ == "__main__":
    cli()

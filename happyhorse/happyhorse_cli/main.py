#!/usr/bin/env python3
"""
HappyHorse CLI - AI Video Generation via AceDataCloud API.

A command-line tool for generating AI videos using HappyHorse
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from happyhorse_cli.commands.info import config, models
from happyhorse_cli.commands.task import task, tasks_batch, wait
from happyhorse_cli.commands.video import generate, image_to_video, reference_to_video, video_edit

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("happyhorse-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="happyhorse-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """HappyHorse CLI - AI Video Generation powered by AceDataCloud.

    Generate AI videos from the command line using HappyHorse models.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      happyhorse generate "A horse galloping through a field"
      happyhorse image-to-video "Animate this" --image-url https://example.com/img.jpg
      happyhorse reference-to-video "Create scene" --image-urls https://example.com/ref.jpg
      happyhorse video-edit "Add music" --video-url https://example.com/video.mp4
      happyhorse task abc123-def456
      happyhorse wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(image_to_video)
cli.add_command(reference_to_video)
cli.add_command(video_edit)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

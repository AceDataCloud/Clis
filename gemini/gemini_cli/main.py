#!/usr/bin/env python3
"""
Gemini CLI - Gemini AI via AceDataCloud.

A command-line tool for Gemini AI chat completions and video generation
powered by AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from gemini_cli.commands.chat import chat
from gemini_cli.commands.info import aspect_ratios, config, models
from gemini_cli.commands.task import task, tasks_batch, wait
from gemini_cli.commands.video import generate, image_to_video, video_to_video

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("gemini-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="gemini-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Gemini CLI - Gemini AI powered by AceDataCloud.

    Chat with Gemini models and generate videos from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      gemini chat "What is the capital of France?"
      gemini generate "A cinematic sunset over the ocean"
      gemini task abc123-def456
      gemini wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(generate)
cli.add_command(image_to_video)
cli.add_command(video_to_video)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)
cli.add_command(aspect_ratios)


if __name__ == "__main__":
    cli()

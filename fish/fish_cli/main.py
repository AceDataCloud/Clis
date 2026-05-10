#!/usr/bin/env python3
"""
Fish CLI - AI Audio Generation via AceDataCloud API.

A command-line tool for generating AI audio using Fish TTS
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from fish_cli.commands.audio import generate
from fish_cli.commands.info import config, models
from fish_cli.commands.task import task, tasks_batch, wait
from fish_cli.commands.voice import clone_voice

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("fish-pro-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="fish-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Fish CLI - AI Audio Generation powered by AceDataCloud.

    Generate AI audio and clone voices from the command line using Fish TTS.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      fish generate "Hello, world!" --voice-id d7900c21663f485ab63ebdb7e5905036
      fish clone-voice --voice-url https://example.com/sample.mp3 --title "My Voice"
      fish task abc123-def456
      fish wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(clone_voice)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

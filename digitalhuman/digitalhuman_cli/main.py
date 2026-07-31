#!/usr/bin/env python3
"""
Digital Human CLI - AI Video Generation via AceDataCloud API.

A command-line tool for generating digital human videos using
the AceDataCloud Digital Human service.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from digitalhuman_cli.commands.info import config, engines
from digitalhuman_cli.commands.task import task, tasks_batch, wait
from digitalhuman_cli.commands.video import generate
from digitalhuman_cli.commands.voice import clone_voice

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("digitalhuman-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="digitalhuman-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Digital Human CLI - AI Video Generation powered by AceDataCloud.

    Generate talking-head videos from a face video/image and audio from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      digitalhuman generate --video-url https://example.com/face.mp4 \\
                            --audio-url https://example.com/speech.mp3
      digitalhuman clone-voice --audio-url https://example.com/voice.wav
      digitalhuman task task_49af42c410c24f04ad416b28af55d237
      digitalhuman wait task_abc123 --interval 5

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
cli.add_command(engines)
cli.add_command(config)


if __name__ == "__main__":
    cli()

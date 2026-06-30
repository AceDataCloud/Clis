#!/usr/bin/env python3
"""
Fish CLI - Text-to-Speech generation via AceDataCloud Fish Audio API.

A command-line tool for Fish Audio TTS generation and voice model management
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from fish_cli.commands.info import config, tts_models
from fish_cli.commands.model import model, models
from fish_cli.commands.task import task, tasks_batch, wait
from fish_cli.commands.tts import tts

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("fish-cli")
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
    """Fish CLI - Text-to-Speech powered by AceDataCloud Fish Audio.

    Generate TTS audio and manage voice models from the command line.

    Get your API token at https://platform.acedata.cloud

    \\b
    Examples:
      fish tts "Hello, world!"
      fish tts "Hello" --reference-id d7900c21663f485ab63ebdb7e5905036
      fish models
      fish model d7900c21663f485ab63ebdb7e5905036
      fish task 2725a2d3-f87e-4905-9c53-9988d5a7b2f5
      fish wait 2725a2d3 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(tts)
cli.add_command(models)
cli.add_command(model)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(tts_models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

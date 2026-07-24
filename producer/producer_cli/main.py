#!/usr/bin/env python3
"""
Producer CLI - AI Music Generation via AceDataCloud API.

A command-line tool for generating AI music using Producer
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from producer_cli.commands.audio import (
    cover,
    extend,
    generate,
    replace_section,
    stems,
    swap_instrumentals,
    swap_vocals,
    variation,
)
from producer_cli.commands.info import actions, config, models
from producer_cli.commands.lyrics import lyrics
from producer_cli.commands.media import upload, video, wav
from producer_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("producer-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="producer-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Producer CLI - AI Music Generation powered by AceDataCloud.

    Generate AI music, lyrics, and manage audio projects from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      producer generate "A happy upbeat pop song about summer"
      producer lyrics "A love song about the ocean"
      producer task abc123-def456
      producer wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands — audio generation
cli.add_command(generate)
cli.add_command(cover)
cli.add_command(extend)
cli.add_command(variation)
cli.add_command(swap_vocals)
cli.add_command(swap_instrumentals)
cli.add_command(replace_section)
cli.add_command(stems)

# Register commands — lyrics
cli.add_command(lyrics)

# Register commands — media
cli.add_command(upload)
cli.add_command(video)
cli.add_command(wav)

# Register commands — tasks
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)

# Register commands — info
cli.add_command(models)
cli.add_command(actions)
cli.add_command(config)


if __name__ == "__main__":
    cli()

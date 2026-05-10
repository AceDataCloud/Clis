#!/usr/bin/env python3
"""
Fish CLI - AI Text-to-Speech via AceDataCloud API.

A command-line tool for generating AI speech using Fish
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from fish_cli.commands.info import config, formats, models
from fish_cli.commands.task import task, tasks_batch, wait
from fish_cli.commands.tts import tts
from fish_cli.commands.voice import voice, voices

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
    """Fish CLI - AI Text-to-Speech powered by AceDataCloud.

    Convert text to speech from the command line using Fish AI models.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      fish tts "Hello, world!"
      fish tts "Hello" --reference-id <voice-id> --format wav
      fish voices --language en
      fish voice <voice-id>
      fish task abc123-def456
      fish wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands — TTS
cli.add_command(tts)

# Register commands — Voice models
cli.add_command(voices)
cli.add_command(voice)

# Register commands — Tasks
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)

# Register commands — Info
cli.add_command(models)
cli.add_command(formats)
cli.add_command(config)


if __name__ == "__main__":
    cli()

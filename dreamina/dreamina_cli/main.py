#!/usr/bin/env python3
"""
Dreamina CLI - AI Video Generation via AceDataCloud API.

A command-line tool for generating AI talking-head videos using Dreamina
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from dreamina_cli.commands.info import config, models
from dreamina_cli.commands.task import task, tasks_batch, wait
from dreamina_cli.commands.video import generate

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("dreamina-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="dreamina-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Dreamina CLI - AI Video Generation powered by AceDataCloud.

    Generate talking-head videos from portrait images and audio from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      dreamina generate --image-url https://example.com/portrait.jpg \\
                        --audio-url https://example.com/speech.mp3
      dreamina task abc123-def456
      dreamina wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

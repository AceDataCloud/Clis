#!/usr/bin/env python3
"""
Veo CLI - AI Veo Video Generation via AceDataCloud API.

A command-line tool for generating AI videos using Veo
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from veo_cli.commands.info import aspect_ratios, config, models
from veo_cli.commands.task import task, tasks_batch, wait
from veo_cli.commands.video import extend, generate, image_to_video, ingredients_to_video, objects, reshoot, upscale

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("veo-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="veo-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Veo CLI - AI Video Generation powered by AceDataCloud.

    Generate AI videos from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      veo generate "A cinematic scene of a sunset over the ocean"
      veo task abc123-def456
      veo wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(image_to_video)
cli.add_command(ingredients_to_video)
cli.add_command(upscale)
cli.add_command(extend)
cli.add_command(reshoot)
cli.add_command(objects)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(models)
cli.add_command(config)
cli.add_command(aspect_ratios)


if __name__ == "__main__":
    cli()

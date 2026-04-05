#!/usr/bin/env python3
"""
Flux CLI - AI Image Generation via AceDataCloud API.

A command-line tool for generating and editing AI images using Flux
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from flux_cli.commands.image import aspect_ratios, edit, generate
from flux_cli.commands.info import config, models
from flux_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("flux-pro-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="flux-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Flux CLI - AI Image Generation powered by AceDataCloud.

    Generate and edit AI images from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      flux generate "A sunset over mountains, photorealistic"
      flux edit "Add a rainbow" --image-url https://example.com/photo.jpg
      flux task abc123-def456
      flux wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(generate)
cli.add_command(edit)
cli.add_command(aspect_ratios)
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)
cli.add_command(config)
cli.add_command(models)


if __name__ == "__main__":
    cli()

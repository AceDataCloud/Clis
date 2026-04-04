#!/usr/bin/env python3
"""
NanoBanana CLI - AI Image Generation via AceDataCloud API.

A command-line tool for generating and editing AI images using NanoBanana
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from nanobanana_cli.commands.image import edit, generate
from nanobanana_cli.commands.info import aspect_ratios, config, models, resolutions
from nanobanana_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("nano-banana-pro-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="nano-banana-pro-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """NanoBanana CLI - AI Image Generation powered by AceDataCloud.

    Generate and edit AI images from the command line using Gemini-powered models.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      nano-banana-pro generate "A cat sitting on a windowsill at sunset"
      nano-banana-pro edit "Make it look like a painting" -i image.jpg
      nano-banana-pro task abc123-def456
      nano-banana-pro wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands — image generation & editing
cli.add_command(generate)
cli.add_command(edit)

# Register commands — tasks
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)

# Register commands — info
cli.add_command(models)
cli.add_command(aspect_ratios)
cli.add_command(resolutions)
cli.add_command(config)


if __name__ == "__main__":
    cli()

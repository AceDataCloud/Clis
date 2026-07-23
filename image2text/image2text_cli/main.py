#!/usr/bin/env python3
"""
Image2Text CLI - English numerical captcha recognition via AceDataCloud API.

A command-line tool for recognizing text from captcha images
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from image2text_cli.commands.captcha import recognize
from image2text_cli.commands.info import config

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("image2text-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="image2text-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """Image2Text CLI - captcha text recognition powered by AceDataCloud.

    Recognize text from captcha images from the command line.

    Get your API token at https://platform.acedata.cloud

    \\b
    Examples:
      image2text recognize /9j/4AAQSkZJRgAB...

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


# Register commands
cli.add_command(recognize)
cli.add_command(config)


if __name__ == "__main__":
    cli()

#!/usr/bin/env python3
"""
Kickart CLI - E-commerce video generation via AceDataCloud API.

A command-line tool for generating e-commerce videos
through the AceDataCloud Kickart platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from kickart_cli.commands.info import config
from kickart_cli.commands.video import template_video, video, viral_video

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("kickart-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="kickart-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """Kickart CLI - E-commerce video generation powered by AceDataCloud.

    Generate e-commerce, viral, and template videos from the command line.

    Get your API token at https://platform.acedata.cloud

    \\b
    Examples:
      kickart video --duration 15 --product-url https://example.com/product
      kickart viral-video --ref-video https://example.com/ref.mp4 --language en
      kickart template-video --template-id tmpl_123 --resource '[...]'

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


# Register commands
cli.add_command(video)
cli.add_command(viral_video)
cli.add_command(template_video)
cli.add_command(config)


if __name__ == "__main__":
    cli()

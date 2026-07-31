#!/usr/bin/env python3
"""
QRArt CLI - Art QR Code Generation via AceDataCloud API.

A command-line tool for generating artistic QR codes using
the AceDataCloud QRArt service.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from qrart_cli.commands.generate import generate
from qrart_cli.commands.info import config, presets
from qrart_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("qrart-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="qrart-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """QRArt CLI - Art QR Code Generation powered by AceDataCloud.

    Generate beautiful artistic QR codes from text prompts.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      qrart generate "A sunset over the ocean" --content https://example.com
      qrart generate "Futuristic city" --content https://example.com --preset neon-mech
      qrart task abc123-def456
      qrart wait abc123 --interval 5

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
cli.add_command(presets)
cli.add_command(config)


if __name__ == "__main__":
    cli()

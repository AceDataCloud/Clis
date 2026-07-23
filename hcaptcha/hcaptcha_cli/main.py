#!/usr/bin/env python3
"""
hCaptcha CLI - hCaptcha verification via AceDataCloud API.

A command-line tool for hCaptcha recognition and token generation
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from hcaptcha_cli.commands.captcha import recognize, token
from hcaptcha_cli.commands.info import config

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("hcaptcha-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="hcaptcha-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """hCaptcha CLI - hCaptcha verification powered by AceDataCloud.

    Recognize captcha images and retrieve bypass tokens from the command line.

    Get your API token at https://platform.acedata.cloud

    \\b
    Examples:
      hcaptcha recognize --queries '["https://example.com/img.jpg"]' --question "Select cars"
      hcaptcha token a5f74b19-9e45-40e0-b45d-47ff91b7a6c2 https://accounts.hcaptcha.com/demo

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


# Register commands
cli.add_command(recognize)
cli.add_command(token)
cli.add_command(config)


if __name__ == "__main__":
    cli()

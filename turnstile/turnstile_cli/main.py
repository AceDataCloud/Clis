#!/usr/bin/env python3
"""
Turnstile CLI - Cloudflare Turnstile captcha bypass via AceDataCloud API.

A command-line tool for retrieving Cloudflare Turnstile tokens
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from turnstile_cli.commands.captcha import token
from turnstile_cli.commands.info import config

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("turnstile-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="turnstile-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """Turnstile CLI - Cloudflare Turnstile bypass powered by AceDataCloud.

    Retrieve Cloudflare Turnstile tokens from the command line.

    Get your API token at https://platform.acedata.cloud

    \\b
    Examples:
      turnstile token 0x4AAAAAAADnPIDROrmt1Wwj https://react-turnstile.vercel.app
      turnstile token 0x4AAAAAAADnPIDROrmt1Wwj https://example.com --action login

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


# Register commands
cli.add_command(token)
cli.add_command(config)


if __name__ == "__main__":
    cli()

#!/usr/bin/env python3
"""
Kimi CLI - Kimi chat completions via AceDataCloud.

A command-line tool for Kimi chat completions powered by AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from kimi_cli.commands.chat import chat
from kimi_cli.commands.info import config, models

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("kimi-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="kimi-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Kimi CLI - Kimi chat completions via AceDataCloud.

    Chat with Kimi models.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      kimi-cli chat "What is the capital of France?"
      kimi-cli chat "Explain AI" -m kimi-k2-thinking

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


cli.add_command(chat)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

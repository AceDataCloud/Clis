#!/usr/bin/env python3
"""
Gemini CLI - Gemini Chat Completions via AceDataCloud.

A command-line tool for Gemini chat completions powered by AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from gemini_cli.commands.chat import chat
from gemini_cli.commands.info import config, models

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("gemini-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="gemini-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Gemini CLI - Gemini Chat Completions via AceDataCloud.

    Chat with Gemini models from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      gemini chat "What is the capital of France?"
      gemini chat "Explain AI" -m gemini-3.1-pro
      gemini models

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

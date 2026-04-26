#!/usr/bin/env python3
"""
Gemini CLI - Gemini AI via AceDataCloud.

A command-line tool for chat completions and content generation
powered by Google Gemini models via AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from gemini_cli.commands.chat import chat
from gemini_cli.commands.generate import generate
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
    """Gemini CLI - Gemini AI via AceDataCloud.

    Chat with Gemini models or generate content using the native Gemini API.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      gemini-cli chat "What is the capital of France?"
      gemini-cli chat "Explain AI" -m gemini-2.5-pro
      gemini-cli generate "Write a poem about the ocean"
      gemini-cli models

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(generate)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

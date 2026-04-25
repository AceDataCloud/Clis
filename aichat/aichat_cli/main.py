#!/usr/bin/env python3
"""
AiChat CLI - AI Dialogue via AceDataCloud API.

A command-line tool for conversing with powerful LLMs
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from aichat_cli.commands.chat import chat
from aichat_cli.commands.info import config, models

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("aichat-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="aichat-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """AiChat CLI - AI Dialogue powered by AceDataCloud.

    Chat with powerful LLMs from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      aichat chat "What is the capital of France?"
      aichat chat "Explain AI" -m gpt-4o
      aichat chat "Hello!" --stateful
      aichat chat "Continue" --stateful --id <conversation-id>

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

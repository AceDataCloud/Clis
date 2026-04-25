#!/usr/bin/env python3
"""
AiChat CLI - AI Dialogue via AceDataCloud API.

A command-line tool for chatting with large language models
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

    Chat with GPT, DeepSeek, Grok, GLM, and more from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      aichat chat "What is the capital of France?"
      aichat chat "Explain AI" -m gpt-4o
      aichat chat "Tell me more" --id <conversation-id>
      aichat models

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

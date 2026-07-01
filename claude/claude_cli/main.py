#!/usr/bin/env python3
"""
Claude CLI - Claude AI via AceDataCloud.

A command-line tool for chatting with Claude models through the
AceDataCloud platform, supporting both the OpenAI-compatible and
native Claude Messages API.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from claude_cli.commands.chat import chat
from claude_cli.commands.info import config, models
from claude_cli.commands.messages import count_tokens, messages

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("claude-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="claude-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Claude CLI - Claude AI powered by AceDataCloud.

    Chat with Claude models from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      claude chat "What is the capital of France?"
      claude chat "Explain AI" -m claude-3-5-sonnet-20241022
      claude messages "Tell me a joke" --max-tokens 1024
      claude count-tokens "Hello, how are you?"
      claude models

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(messages)
cli.add_command(count_tokens)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

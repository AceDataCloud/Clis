#!/usr/bin/env python3
"""
Claude CLI - Claude AI via AceDataCloud.

A command-line tool for chat completions, messages, and token counting
powered by Anthropic Claude models via AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from claude_cli.commands.chat import chat
from claude_cli.commands.count_tokens import count_tokens
from claude_cli.commands.info import config, models
from claude_cli.commands.messages import messages

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
    """Claude CLI - Claude AI via AceDataCloud.

    Chat with Claude models using OpenAI-compatible or native Messages API.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      claude-cli chat "What is the capital of France?"
      claude-cli chat "Explain AI" -m claude-opus-4-20250514
      claude-cli messages "Write a poem about the ocean"
      claude-cli count-tokens "Hello, how are you?"
      claude-cli models

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(messages)
cli.add_command(count_tokens, name="count-tokens")
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

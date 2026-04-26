#!/usr/bin/env python3
"""
DeepSeek CLI - DeepSeek chat completions via AceDataCloud.

A command-line tool for DeepSeek chat completions powered by AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from deepseek_cli.commands.chat import chat
from deepseek_cli.commands.info import config, models

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("deepseek-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="deepseek-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """DeepSeek CLI - DeepSeek chat completions via AceDataCloud.

    Chat with DeepSeek models.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      deepseek-cli chat "What is the capital of France?"
      deepseek-cli chat "Explain AI" -m deepseek-r1

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

#!/usr/bin/env python3
"""
GLM CLI - GLM Chat Completions via AceDataCloud.

A command-line tool for GLM chat completions powered by AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from glm_cli.commands.chat import chat
from glm_cli.commands.info import config, models

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("glm-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="glm-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """GLM CLI - GLM Chat Completions via AceDataCloud.

    Chat with GLM models from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      glm chat "What is the capital of France?"
      glm chat "Explain AI" -m glm-5.1
      glm models

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

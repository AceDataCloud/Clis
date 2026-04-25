#!/usr/bin/env python3
"""
OpenAI CLI - OpenAI generation via AceDataCloud API.

A command-line tool for accessing OpenAI models (chat, embeddings, image
generation, image editing) through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from openai_cli.commands.chat import chat, complete
from openai_cli.commands.embed import embed
from openai_cli.commands.image import edit_image, imagine
from openai_cli.commands.info import config, models
from openai_cli.commands.respond import respond

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("openai-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="openai-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """OpenAI CLI - OpenAI generation powered by AceDataCloud.

    Access GPT models, embeddings, and image generation from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      openai chat "What is the capital of France?"
      openai imagine "A serene mountain landscape"
      openai embed "The quick brown fox"
      openai respond "Explain quantum computing" -m o3

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(complete)
cli.add_command(embed)
cli.add_command(imagine)
cli.add_command(edit_image)
cli.add_command(respond)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

#!/usr/bin/env python3
"""
OpenAI CLI - OpenAI-compatible APIs via AceDataCloud.

A command-line tool for chat completions, embeddings, image generation,
image editing, and the Responses API powered by AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from openai_cli.commands.chat import chat
from openai_cli.commands.embed import embed
from openai_cli.commands.image import edit, image
from openai_cli.commands.info import config, models
from openai_cli.commands.response import response

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
    """OpenAI CLI - OpenAI-compatible APIs via AceDataCloud.

    Chat with GPT models, generate embeddings, create and edit images.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
      openai-cli chat "What is the capital of France?"
      openai-cli chat "Explain AI" -m gpt-5.4
      openai-cli embed "Hello world" -m text-embedding-3-small
      openai-cli image "A sunset over mountains"
      openai-cli edit "Add clouds" --image-url https://example.com/photo.jpg
      openai-cli response "Summarize this topic" -m gpt-4o

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(chat)
cli.add_command(embed)
cli.add_command(image)
cli.add_command(edit)
cli.add_command(response)
cli.add_command(models)
cli.add_command(config)


if __name__ == "__main__":
    cli()

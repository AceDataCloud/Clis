#!/usr/bin/env python3
"""
QwenImage CLI - AI Image Generation via AceDataCloud API.

A command-line tool for generating and editing AI images using QwenImage
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from qwen_image_cli.commands.image import edit, generate
from qwen_image_cli.commands.info import config, models, prompt_extend_modes
from qwen_image_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("qwen-image-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="qwen-image-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """QwenImage CLI - AI Image Generation powered by AceDataCloud.

    Generate and edit AI images from the command line using Qwen Image models.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      qwen-image generate "A cat sitting on a windowsill at sunset"
      qwen-image edit "Make it look like a painting" -i image.jpg
      qwen-image task abc123-def456
      qwen-image wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands — image generation & editing
cli.add_command(generate)
cli.add_command(edit)

# Register commands — tasks
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)

# Register commands — info
cli.add_command(models)
cli.add_command(prompt_extend_modes)
cli.add_command(config)


if __name__ == "__main__":
    cli()

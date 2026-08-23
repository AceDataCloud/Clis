from importlib import metadata

import click
from dotenv import load_dotenv

from qwen_image_cli.commands.image import edit, generate
from qwen_image_cli.commands.info import models
from qwen_image_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def version() -> str:
    try:
        return metadata.version("qwen-image-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=version(), prog_name="qwen-image-cli")
@click.option("--token", envvar="ACEDATACLOUD_API_TOKEN")
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Qwen Image 3 generation and editing CLI."""
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


for command in [generate, edit, task, tasks_batch, wait, models]:
    cli.add_command(command)

if __name__ == "__main__":
    cli()

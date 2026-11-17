"""ACE Music CLI: submit once and query the original task."""

from importlib import metadata

import click

from acemusic_cli.commands.music import generate, lyrics
from acemusic_cli.commands.task import download, history, task, tasks_batch, wait


def get_version() -> str:
    try:
        return metadata.version("acemusic-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version())
@click.option("--token", envvar="ACEDATACLOUD_API_TOKEN", help="Application API key.")
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """ACE Music songs and lyrics through Ace Data Cloud."""
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


@cli.command()
def models() -> None:
    """List public models without a paid request."""
    click.echo("acemusic-v1.1 (default)\nacemusic-v1")


for command in (generate, lyrics, task, tasks_batch, history, wait, download):
    cli.add_command(command)


if __name__ == "__main__":
    cli()

#!/usr/bin/env python3
"""
WebExtrator CLI - Web Render & Extract via AceDataCloud.

A command-line tool for extracting structured content and rendering web pages
powered by AceDataCloud.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from webextrator_cli.commands.info import config
from webextrator_cli.commands.task import tasks
from webextrator_cli.commands.web import extract, render

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("webextrator-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="webextrator-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """WebExtrator CLI - Web Render & Extract via AceDataCloud.

    Extract structured data and render web pages from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      webextrator extract https://www.amazon.com/dp/B0C1234567
      webextrator render https://example.com
      webextrator tasks retrieve --id <task-id>

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(extract)
cli.add_command(render)
cli.add_command(tasks)
cli.add_command(config)


if __name__ == "__main__":
    cli()

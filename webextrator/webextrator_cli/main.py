#!/usr/bin/env python3
"""
WebExtrator CLI - Web Render & Extract via AceDataCloud API.

A command-line tool for rendering and extracting content from web pages
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from webextrator_cli.commands.extract import extract
from webextrator_cli.commands.info import config
from webextrator_cli.commands.render import render
from webextrator_cli.commands.tasks import tasks

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
    """WebExtrator CLI - Web Render & Extract powered by AceDataCloud.

    Render web pages and extract structured content from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Quick start:
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

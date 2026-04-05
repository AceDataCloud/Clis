#!/usr/bin/env python3
"""
SERP CLI - Google Search via AceDataCloud API.

A command-line tool for searching Google using the SERP API
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from serp_cli.commands.info import config, search_types, time_ranges
from serp_cli.commands.search import images, maps, news, places, search, videos

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("serp-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="serp-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """SERP CLI - Google Search powered by AceDataCloud.

    Search Google from the command line with structured results.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      serp search "artificial intelligence"
      serp news "tech news" --time-range qdr:d
      serp images "sunset photography" -n 20
      serp places "coffee shops" -c uk

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands
cli.add_command(search)
cli.add_command(images)
cli.add_command(news)
cli.add_command(videos)
cli.add_command(places)
cli.add_command(maps)
cli.add_command(search_types)
cli.add_command(time_ranges)
cli.add_command(config)


if __name__ == "__main__":
    cli()

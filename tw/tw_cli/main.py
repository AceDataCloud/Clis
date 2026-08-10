#!/usr/bin/env python3
"""Twitter/X CLI - Twitter information via AceDataCloud API."""

from importlib import metadata

import click
from dotenv import load_dotenv

from tw_cli.commands.info import config
from tw_cli.commands.twitter import posts, retweets, users

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("tw-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="tw-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """Twitter/X CLI - Twitter information powered by AceDataCloud."""
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


cli.add_command(posts)
cli.add_command(users)
cli.add_command(retweets)
cli.add_command(config)


if __name__ == "__main__":
    cli()

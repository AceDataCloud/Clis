#!/usr/bin/env python3
"""TikTok CLI - TikTok information via AceDataCloud API."""

from importlib import metadata

import click
from dotenv import load_dotenv

from tiktok_cli.commands.info import config
from tiktok_cli.commands.tiktok import posts, search, user, video

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("tiktok-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="tiktok-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """TikTok CLI - TikTok information powered by AceDataCloud."""
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


cli.add_command(posts)
cli.add_command(search)
cli.add_command(user)
cli.add_command(video)
cli.add_command(config)


if __name__ == "__main__":
    cli()

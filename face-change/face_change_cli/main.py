#!/usr/bin/env python3
"""Face Change CLI - face transformation via AceDataCloud API."""

from importlib import metadata

import click
from dotenv import load_dotenv

from face_change_cli.commands.face import (
    analyze,
    beautify,
    cartoon,
    change_age,
    change_gender,
    detect_live,
    swap,
)
from face_change_cli.commands.info import config

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("face-change-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="face-change-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """Face Change CLI - face transformation powered by AceDataCloud."""
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


cli.add_command(analyze)
cli.add_command(beautify)
cli.add_command(change_age)
cli.add_command(change_gender)
cli.add_command(detect_live)
cli.add_command(swap)
cli.add_command(cartoon)
cli.add_command(config)


if __name__ == "__main__":
    cli()

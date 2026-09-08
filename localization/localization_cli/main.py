#!/usr/bin/env python3
"""
Localization CLI - translation via AceDataCloud API.

A command-line tool for translating markdown and JSON localization content
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from localization_cli.commands.info import config
from localization_cli.commands.translate import translate

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("localization-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="localization-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """Localization CLI - translation powered by AceDataCloud.

    Translate markdown text or JSON localization objects from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      localization translate "# Title" --locale zh-CN
      localization translate '{"message.clickButton":{"message":"Please click"}}' --extension json --locale zh-CN

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


cli.add_command(translate)
cli.add_command(config)


if __name__ == "__main__":
    cli()

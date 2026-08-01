#!/usr/bin/env python3
"""
Discord Bot CLI - Discord Agent Proxy via AceDataCloud.

A command-line tool for interacting with a self-hosted Discord Agent Proxy service.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from discord_bot_cli.commands.account import whoami
from discord_bot_cli.commands.dms import open_dm, send_dm
from discord_bot_cli.commands.guilds import channels, create_channel, guilds, members
from discord_bot_cli.commands.info import config, health
from discord_bot_cli.commands.messages import delete, edit, messages, pin, react, search, send

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("discord-bot-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="discord-bot-cli")
@click.option(
    "--base-url",
    envvar="DISCORD_BOT_BASE_URL",
    help="Discord Bot service base URL (or set DISCORD_BOT_BASE_URL env var).",
)
@click.option(
    "--token",
    envvar="DISCORD_BOT_TOKEN",
    help="Access token (or set DISCORD_BOT_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, base_url: str | None, token: str | None) -> None:
    """Discord Bot CLI - Discord Agent Proxy via AceDataCloud.

    Interact with a self-hosted Discord Agent Proxy from the command line.

    Deploy your own instance at https://platform.acedata.cloud/console/applications

    \\b
    Examples:
      discord-bot health
      discord-bot whoami
      discord-bot guilds
      discord-bot channels 1234567890
      discord-bot send 1234567890 "Hello!"
      discord-bot messages 1234567890

    Set your service URL and token:
      export DISCORD_BOT_BASE_URL=https://discord-bot-xxxx.app.acedata.cloud
      export DISCORD_BOT_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url
    ctx.obj["token"] = token


# Register commands
cli.add_command(health)
cli.add_command(config)
cli.add_command(whoami)
cli.add_command(guilds)
cli.add_command(channels)
cli.add_command(create_channel)
cli.add_command(members)
cli.add_command(send)
cli.add_command(messages)
cli.add_command(search)
cli.add_command(edit)
cli.add_command(delete)
cli.add_command(react)
cli.add_command(pin)
cli.add_command(open_dm)
cli.add_command(send_dm)


if __name__ == "__main__":
    cli()

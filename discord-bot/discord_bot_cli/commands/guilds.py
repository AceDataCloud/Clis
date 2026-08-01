"""Guild, channel, and member commands."""

import click

from discord_bot_cli.core.client import get_client
from discord_bot_cli.core.exceptions import DiscordBotError
from discord_bot_cli.core.output import (
    print_channels,
    print_error,
    print_guilds,
    print_json,
    print_members,
    print_success,
)


@click.command()
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def guilds(ctx: click.Context, output_json: bool) -> None:
    """List guilds (servers) the account has joined.

    \\b
    Examples:
      discord-bot guilds
      discord-bot guilds --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.list_guilds()
        if output_json:
            print_json(result)
        else:
            print_guilds(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("guild_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def channels(ctx: click.Context, guild_id: str, output_json: bool) -> None:
    """List channels in a guild.

    GUILD_ID is the ID of the Discord server.

    \\b
    Examples:
      discord-bot channels 1234567890
      discord-bot channels 1234567890 --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.list_channels(guild_id)
        if output_json:
            print_json(result)
        else:
            print_channels(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("create-channel")
@click.argument("guild_id")
@click.argument("name")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def create_channel(ctx: click.Context, guild_id: str, name: str, output_json: bool) -> None:
    """Create a text channel in a guild.

    GUILD_ID is the ID of the Discord server.
    NAME is the name for the new channel.

    \\b
    Examples:
      discord-bot create-channel 1234567890 general
      discord-bot create-channel 1234567890 announcements --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.create_channel(guild_id, name)
        if output_json:
            print_json(result)
        else:
            print_success(f"Channel '{name}' created.")
            print_json(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("guild_id")
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Maximum number of members to return (default: 100).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def members(ctx: click.Context, guild_id: str, limit: int | None, output_json: bool) -> None:
    """List members of a guild.

    GUILD_ID is the ID of the Discord server.

    \\b
    Examples:
      discord-bot members 1234567890
      discord-bot members 1234567890 --limit 50
      discord-bot members 1234567890 --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.list_members(guild_id, limit=limit)
        if output_json:
            print_json(result)
        else:
            print_members(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e

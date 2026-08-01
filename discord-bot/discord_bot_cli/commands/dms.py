"""Direct message commands."""

import click

from discord_bot_cli.core.client import get_client
from discord_bot_cli.core.exceptions import DiscordBotError
from discord_bot_cli.core.output import print_dm_channel, print_error, print_json, print_message


@click.command("open-dm")
@click.argument("recipient_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def open_dm(ctx: click.Context, recipient_id: str, output_json: bool) -> None:
    """Open a DM channel with a user and return the channel ID.

    RECIPIENT_ID is the Discord user ID to open a DM with.

    \\b
    Examples:
      discord-bot open-dm 111222333444555666
      discord-bot open-dm 111222333444555666 --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.open_dm(recipient_id)
        if output_json:
            print_json(result)
        else:
            print_dm_channel(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("send-dm")
@click.argument("recipient_id")
@click.argument("content")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def send_dm(ctx: click.Context, recipient_id: str, content: str, output_json: bool) -> None:
    """Send a direct message to a user.

    RECIPIENT_ID is the Discord user ID.
    CONTENT is the message text to send.

    \\b
    Examples:
      discord-bot send-dm 111222333444555666 "Hello!"
      discord-bot send-dm 111222333444555666 "Hi there" --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.send_dm(recipient_id, content)
        if output_json:
            print_json(result)
        else:
            print_message(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e

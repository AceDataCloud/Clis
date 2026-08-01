"""Message commands (send, read, edit, delete, react, pin, search)."""

import click

from discord_bot_cli.core.client import get_client
from discord_bot_cli.core.exceptions import DiscordBotError
from discord_bot_cli.core.output import (
    print_error,
    print_json,
    print_message,
    print_messages,
    print_success,
)


@click.command()
@click.argument("channel_id")
@click.argument("content")
@click.option(
    "--reply-to",
    default=None,
    help="Message ID to reply to.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def send(
    ctx: click.Context,
    channel_id: str,
    content: str,
    reply_to: str | None,
    output_json: bool,
) -> None:
    """Send a message to a channel.

    CHANNEL_ID is the ID of the Discord channel.
    CONTENT is the message text to send.

    \\b
    Examples:
      discord-bot send 1234567890 "Hello!"
      discord-bot send 1234567890 "Got it" --reply-to 9876543210
      discord-bot send 1234567890 "Hi" --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.send_message(channel_id, content, reply_to=reply_to)
        if output_json:
            print_json(result)
        else:
            print_message(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("channel_id")
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Number of messages to retrieve (default: 50, max: 100).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def messages(ctx: click.Context, channel_id: str, limit: int | None, output_json: bool) -> None:
    """Read recent messages from a channel.

    CHANNEL_ID is the ID of the Discord channel.

    \\b
    Examples:
      discord-bot messages 1234567890
      discord-bot messages 1234567890 --limit 20
      discord-bot messages 1234567890 --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.read_messages(channel_id, limit=limit)
        if output_json:
            print_json(result)
        else:
            print_messages(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("channel_id")
@click.argument("query")
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Maximum number of results (default: 25).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def search(
    ctx: click.Context,
    channel_id: str,
    query: str,
    limit: int | None,
    output_json: bool,
) -> None:
    """Search messages in a channel.

    CHANNEL_ID is the ID of the Discord channel.
    QUERY is the search term.

    \\b
    Examples:
      discord-bot search 1234567890 "release date"
      discord-bot search 1234567890 "hello" --limit 10
      discord-bot search 1234567890 "update" --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.search_messages(channel_id, query, limit=limit)
        if output_json:
            print_json(result)
        else:
            print_messages(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("channel_id")
@click.argument("message_id")
@click.argument("content")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edit(
    ctx: click.Context,
    channel_id: str,
    message_id: str,
    content: str,
    output_json: bool,
) -> None:
    """Edit a message you sent.

    CHANNEL_ID is the ID of the Discord channel.
    MESSAGE_ID is the ID of the message to edit.
    CONTENT is the new message text.

    \\b
    Examples:
      discord-bot edit 1234567890 9876543210 "Updated text"
      discord-bot edit 1234567890 9876543210 "New content" --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.edit_message(channel_id, message_id, content)
        if output_json:
            print_json(result)
        else:
            print_message(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("channel_id")
@click.argument("message_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def delete(
    ctx: click.Context,
    channel_id: str,
    message_id: str,
    output_json: bool,
) -> None:
    """Delete a message.

    CHANNEL_ID is the ID of the Discord channel.
    MESSAGE_ID is the ID of the message to delete.

    \\b
    Examples:
      discord-bot delete 1234567890 9876543210
      discord-bot delete 1234567890 9876543210 --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.delete_message(channel_id, message_id)
        if output_json:
            print_json(result)
        else:
            print_success(f"Message {message_id} deleted.")
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("channel_id")
@click.argument("message_id")
@click.argument("emoji")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def react(
    ctx: click.Context,
    channel_id: str,
    message_id: str,
    emoji: str,
    output_json: bool,
) -> None:
    """Add a reaction to a message.

    CHANNEL_ID is the ID of the Discord channel.
    MESSAGE_ID is the ID of the message.
    EMOJI is the emoji to react with (e.g. 👍 or :thumbsup:).

    \\b
    Examples:
      discord-bot react 1234567890 9876543210 "👍"
      discord-bot react 1234567890 9876543210 "🎉" --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.add_reaction(channel_id, message_id, emoji)
        if output_json:
            print_json(result)
        else:
            print_success(f"Reaction {emoji} added to message {message_id}.")
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("channel_id")
@click.argument("message_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def pin(
    ctx: click.Context,
    channel_id: str,
    message_id: str,
    output_json: bool,
) -> None:
    """Pin a message in a channel.

    CHANNEL_ID is the ID of the Discord channel.
    MESSAGE_ID is the ID of the message to pin.

    \\b
    Examples:
      discord-bot pin 1234567890 9876543210
      discord-bot pin 1234567890 9876543210 --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.pin_message(channel_id, message_id)
        if output_json:
            print_json(result)
        else:
            print_success(f"Message {message_id} pinned.")
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e

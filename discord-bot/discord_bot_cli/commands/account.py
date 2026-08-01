"""Account info command."""

import click

from discord_bot_cli.core.client import get_client
from discord_bot_cli.core.exceptions import DiscordBotError
from discord_bot_cli.core.output import print_error, print_json, print_whoami


@click.command()
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def whoami(ctx: click.Context, output_json: bool) -> None:
    """Show the current proxied Discord account.

    \\b
    Examples:
      discord-bot whoami
      discord-bot whoami --json
    """
    client = get_client(base_url=ctx.obj.get("base_url"), token=ctx.obj.get("token"))
    try:
        result = client.whoami()
        if output_json:
            print_json(result)
        else:
            print_whoami(result)
    except DiscordBotError as e:
        print_error(e.message)
        raise SystemExit(1) from e

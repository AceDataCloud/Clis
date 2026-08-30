"""Twitter/X information commands."""

from typing import Any

import click

from tw_cli.core.client import get_client
from tw_cli.core.exceptions import TwError
from tw_cli.core.output import print_error, print_json, print_result


def _emit(client_method: Any, payload: dict[str, object], output_json: bool, title: str) -> None:
    """Call a client method and print the result."""
    try:
        result = client_method(**payload)
        if output_json:
            print_json(result)
        else:
            print_result(result, title=title)
    except TwError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("user_id")
@click.option("--cursor", default=None, help="Pagination cursor.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def posts(ctx: click.Context, user_id: str, cursor: str | None, output_json: bool) -> None:
    """Get post information for a Twitter/X user."""
    payload: dict[str, object] = {"user_id": user_id, "cursor": cursor}
    _emit(get_client(ctx.obj.get("token")).posts, payload, output_json, "Posts Result")


@click.command()
@click.argument("username")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def users(ctx: click.Context, username: str, output_json: bool) -> None:
    """Get Twitter/X user details by username."""
    _emit(get_client(ctx.obj.get("token")).users, {"username": username}, output_json, "Users Result")


@click.command()
@click.argument("post_id")
@click.option("--cursor", default=None, help="Pagination cursor.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def retweets(ctx: click.Context, post_id: str, cursor: str | None, output_json: bool) -> None:
    """Find retweets of a tweet."""
    payload: dict[str, object] = {"post_id": post_id, "cursor": cursor}
    _emit(get_client(ctx.obj.get("token")).retweets, payload, output_json, "Retweets Result")


@click.command()
@click.argument("note_id")
@click.option("--cursor", default=None, help="Pagination cursor.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def comments(ctx: click.Context, note_id: str, cursor: str | None, output_json: bool) -> None:
    """Get all the comment information for a tweet by entering the id of the tweet."""
    payload: dict[str, object] = {"note_id": note_id, "cursor": cursor}
    _emit(get_client(ctx.obj.get("token")).comments, payload, output_json, "Comments Result")


@click.command()
@click.argument("keyword")
@click.option("--cursor", default=None, help="Pagination cursor.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def search(ctx: click.Context, keyword: str, cursor: str | None, output_json: bool) -> None:
    """Find chronological tweets by keyword."""
    payload: dict[str, object] = {"keyword": keyword, "cursor": cursor}
    _emit(get_client(ctx.obj.get("token")).search, payload, output_json, "Search Result")

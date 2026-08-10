"""TikTok information commands."""

from typing import Any

import click

from tiktok_cli.core.client import get_client
from tiktok_cli.core.exceptions import TikTokError
from tiktok_cli.core.output import print_error, print_json, print_result

SEARCH_TYPES = ["user", "video"]
REGIONS = ["us", "jp", "kr", "vn", "br", "ru"]
SORT_TYPES = ["0", "1", "3"]
PUBLISH_TIMES = ["0", "1", "24", "7", "30", "90", "180"]


def _emit(client_method: Any, payload: dict[str, object], output_json: bool, title: str) -> None:
    """Call a client method and print the result."""
    try:
        result = client_method(**payload)
        if output_json:
            print_json(result)
        else:
            print_result(result, title=title)
    except TikTokError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.option("--cursor", default=None, help="Pagination cursor.")
@click.option("--user-id", default=None, help="TikTok user ID.")
@click.option("--unique-id", default=None, help="TikTok unique ID.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def posts(
    ctx: click.Context,
    cursor: str | None,
    user_id: str | None,
    unique_id: str | None,
    output_json: bool,
) -> None:
    """Get a TikTok user's posts."""
    payload: dict[str, object] = {"cursor": cursor, "user_id": user_id, "unique_id": unique_id}
    _emit(get_client(ctx.obj.get("token")).posts, payload, output_json, "Posts Result")


@click.command()
@click.argument("keywords")
@click.option("--type", "search_type", type=click.Choice(SEARCH_TYPES), required=True, help="Search type.")
@click.option("--cursor", type=int, default=None, help="Pagination cursor.")
@click.option("--region", type=click.Choice(REGIONS), default=None, help="Search region.")
@click.option("--sort-type", type=click.Choice(SORT_TYPES), default=None, help="Sort type.")
@click.option("--publish-time", type=click.Choice(PUBLISH_TIMES), default=None, help="Publish time filter.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def search(
    ctx: click.Context,
    keywords: str,
    search_type: str,
    cursor: int | None,
    region: str | None,
    sort_type: str | None,
    publish_time: str | None,
    output_json: bool,
) -> None:
    """Search TikTok users or videos by keyword."""
    payload: dict[str, object] = {
        "type": search_type,
        "keywords": keywords,
        "cursor": cursor,
        "region": region,
        "sort_type": int(sort_type) if sort_type is not None else None,
        "publish_time": int(publish_time) if publish_time is not None else None,
    }
    _emit(get_client(ctx.obj.get("token")).search, payload, output_json, "Search Result")


@click.command()
@click.option("--cursor", default=None, help="Pagination cursor.")
@click.option("--user-id", default=None, help="TikTok user ID.")
@click.option("--unique-id", default=None, help="TikTok unique ID.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def user(
    ctx: click.Context,
    cursor: str | None,
    user_id: str | None,
    unique_id: str | None,
    output_json: bool,
) -> None:
    """Get TikTok user details."""
    payload: dict[str, object] = {"cursor": cursor, "user_id": user_id, "unique_id": unique_id}
    _emit(get_client(ctx.obj.get("token")).user, payload, output_json, "User Result")


@click.command()
@click.argument("video_url")
@click.option("--original-quality", type=int, default=None, help="Original quality flag.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def video(
    ctx: click.Context,
    video_url: str,
    original_quality: int | None,
    output_json: bool,
) -> None:
    """Get TikTok video details."""
    payload: dict[str, object] = {"video_url": video_url, "original_quality": original_quality}
    _emit(get_client(ctx.obj.get("token")).video, payload, output_json, "Video Result")

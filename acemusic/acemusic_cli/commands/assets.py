"""Manage owned ACE Music reference assets."""

from typing import Any
from urllib.parse import urlsplit

import click

from acemusic_cli.core.client import get_client
from acemusic_cli.core.exceptions import AceMusicError
from acemusic_cli.core.output import print_json

ASSET_TYPES = click.Choice(["midi", "image", "video"])


@click.group()
def assets() -> None:
    """Import, inspect and list your MIDI, image and video references."""


def _request(ctx: click.Context, payload: dict[str, Any], key: str | None = None) -> None:
    try:
        result = get_client(ctx.obj.get("token")).request(
            "/acemusic/assets", payload, idempotency_key=key
        )
    except AceMusicError as error:
        raise click.ClickException(error.message) from error
    print_json(result)


@assets.command()
@click.argument("url")
@click.option("--type", "asset_type", type=ASSET_TYPES, required=True)
@click.option("--name", help="Optional display name.")
@click.option("--callback-url", help="A real webhook you control.")
@click.option("--idempotency-key", help="Stable key for this import.")
@click.pass_context
def upload(
    ctx: click.Context,
    url: str,
    asset_type: str,
    name: str | None,
    callback_url: str | None,
    idempotency_key: str | None,
) -> None:
    """Submit one paid asset import where the selected type is enabled."""
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.fragment
    ):
        raise click.UsageError("Use a public HTTPS URL without embedded credentials or a fragment.")
    payload = {"action": "upload", "type": asset_type, "url": url, "async": True}
    if name is not None:
        payload["name"] = name
    if callback_url is not None:
        payload["callback_url"] = callback_url
    _request(ctx, payload, idempotency_key)


@assets.command()
@click.argument("id")
@click.pass_context
def get(ctx: click.Context, id: str) -> None:
    """Read one asset by platform asset ID for free."""
    if not id.strip():
        raise click.UsageError("An asset ID is required.")
    _request(ctx, {"action": "retrieve", "id": id})


@assets.command("list")
@click.option("--page", type=click.IntRange(1), default=1, show_default=True)
@click.option("--page-size", type=click.IntRange(1, 100), default=20, show_default=True)
@click.option("--type", "asset_type", type=ASSET_TYPES, help="Only return this type.")
@click.pass_context
def list_assets(ctx: click.Context, page: int, page_size: int, asset_type: str | None) -> None:
    """List your asset history for free."""
    payload = {"action": "retrieve", "page": page, "page_size": page_size}
    if asset_type is not None:
        payload["type"] = asset_type
    _request(ctx, payload)

"""Paid music and lyrics submissions."""

from math import isfinite
from pathlib import Path
from typing import Any

import click

from acemusic_cli.core.client import get_client
from acemusic_cli.core.exceptions import AceMusicError
from acemusic_cli.core.output import print_json


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "--model",
    type=click.Choice(["acemusic-v1.1", "acemusic-v1"]),
    default="acemusic-v1.1",
    show_default=True,
)
@click.option(
    "--lyric-file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="UTF-8 custom lyrics file.",
)
@click.option("--style", help="Required with custom lyrics.")
@click.option("--title", default="", help="Required with custom lyrics.")
@click.option("--callback-url", help="A real webhook you control.")
@click.option("--json", "output_json", is_flag=True, help="Print JSON (the default).")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str | None,
    model: str,
    lyric_file: Path | None,
    style: str | None,
    title: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Submit ONE paid task targeting two song candidates, then save task_id.

    Pass PROMPT for idea mode, or --lyric-file, --style and --title for custom mode.
    No automatic retry is made if submission times out.
    """
    del output_json
    payload: dict[str, Any] = {
        "action": "generate",
        "model": model,
        "custom": lyric_file is not None,
        "async": True,
    }
    if lyric_file:
        if prompt or not style or not style.strip() or not title.strip():
            raise click.UsageError(
                "Custom mode requires --lyric-file, --style and --title, without PROMPT."
            )
        lyric = lyric_file.read_text(encoding="utf-8")
        if not lyric.strip():
            raise click.UsageError("The lyrics file is empty.")
        payload.update(lyric=lyric, style=style, title=title)
    else:
        if not prompt or style or title:
            raise click.UsageError(
                "Idea mode requires PROMPT; custom style/title require --lyric-file."
            )
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url
    try:
        print_json(get_client(ctx.obj.get("token")).generate_audio(**payload))
    except AceMusicError as error:
        raise click.ClickException(
            error.message + " Preserve the original request; do not automatically submit again."
        ) from error


@click.command()
@click.argument("prompt")
@click.option("--style", default="")
@click.option("--json", "output_json", is_flag=True, help="Print JSON (the default).")
@click.pass_context
def lyrics(ctx: click.Context, prompt: str, style: str, output_json: bool) -> None:
    """Generate lyrics and a title as a separately priced request."""
    del output_json
    try:
        print_json(
            get_client(ctx.obj.get("token")).generate_lyrics(
                prompt=prompt, **({"style": style} if style else {})
            )
        )
    except AceMusicError as error:
        raise click.ClickException(error.message) from error


def _submit_reference(ctx: click.Context, payload: dict[str, Any]) -> None:
    try:
        print_json(get_client(ctx.obj.get("token")).generate_audio(**payload))
    except AceMusicError as error:
        raise click.ClickException(
            error.message + " Preserve the original request; do not automatically submit again."
        ) from error


@click.command("upload")
@click.argument("audio_url")
@click.option("--name", help="Display name for this separate priced import.")
@click.option("--audio-id", help="Optional caller-owned platform audio ID anchor.")
@click.option("--callback-url", help="A real webhook you control.")
@click.pass_context
def upload_audio(
    ctx: click.Context,
    audio_url: str,
    name: str | None,
    audio_id: str | None,
    callback_url: str | None,
) -> None:
    """Import ONE owned audio URL; do not create a cover automatically."""
    from urllib.parse import urlsplit

    parsed = urlsplit(audio_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise click.UsageError("A public HTTPS MP3 URL without credentials is required.")
    payload: dict[str, Any] = {"action": "upload", "audio_url": audio_url, "async": True}
    for key, value in (("name", name), ("audio_id", audio_id), ("callback_url", callback_url)):
        if value:
            payload[key] = value
    _submit_reference(ctx, payload)


def _reference_options(function: Any) -> Any:
    options = [
        click.option(
            "--lyric-file",
            type=click.Path(exists=True, dir_okay=False, path_type=Path),
            required=True,
        ),
        click.option("--style", required=True),
        click.option("--title", help="Optional title for the new songs."),
        click.option(
            "--audio-influence", type=click.FloatRange(1, 100), default=60, show_default=True
        ),
        click.option("--callback-url", help="A real webhook you control."),
    ]
    for option in reversed(options):
        function = option(function)
    return function


def _reference_payload(
    action: str,
    lyric_file: Path,
    style: str,
    title: str | None,
    audio_influence: float,
    callback_url: str | None,
) -> dict[str, Any]:
    if not isfinite(audio_influence) or not 1 <= audio_influence <= 100:
        raise click.UsageError("Audio influence must be a finite number from 1 to 100.")
    lyric = lyric_file.read_text(encoding="utf-8")
    if not lyric.strip() or not style.strip():
        raise click.UsageError("Nonempty lyrics and style are required.")
    payload: dict[str, Any] = {
        "action": action,
        "model": "acemusic-v1.1",
        "lyric": lyric,
        "style": style,
        "audio_influence": audio_influence,
        "async": True,
    }
    if title:
        payload["title"] = title
    if callback_url:
        payload["callback_url"] = callback_url
    return payload


@click.command("cover")
@click.argument("audio_id")
@_reference_options
@click.pass_context
def cover_audio(
    ctx: click.Context,
    audio_id: str,
    lyric_file: Path,
    style: str,
    title: str | None,
    audio_influence: float,
    callback_url: str | None,
) -> None:
    """Submit ONE paid cover from a successful caller-owned platform audio ID."""
    payload = _reference_payload("cover", lyric_file, style, title, audio_influence, callback_url)
    payload["audio_id"] = audio_id
    _submit_reference(ctx, payload)


@click.command("mashup")
@click.argument("audio_ids", nargs=2)
@_reference_options
@click.pass_context
def mashup_audio(
    ctx: click.Context,
    audio_ids: tuple[str, str],
    lyric_file: Path,
    style: str,
    title: str | None,
    audio_influence: float,
    callback_url: str | None,
) -> None:
    """Submit ONE paid mashup from two compatible owned platform audio IDs."""
    if len(set(audio_ids)) != 2:
        raise click.UsageError("Two distinct platform audio IDs are required.")
    payload = _reference_payload("mashup", lyric_file, style, title, audio_influence, callback_url)
    payload["mashup_audio_ids"] = list(audio_ids)
    _submit_reference(ctx, payload)

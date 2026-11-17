"""Paid music and lyrics submissions."""

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

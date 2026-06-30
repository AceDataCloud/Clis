"""Lip-sync and talking-photo generation commands."""

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import print_error, print_json, print_video_result

TALKING_PHOTO_MODELS = [
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
]


def _validate_duration(
    _ctx: click.Context, _param: click.Parameter, value: int | None
) -> int | None:
    """Validate talking-photo duration."""
    if value is None or value in {5, 10}:
        return value
    raise click.BadParameter("Must be 5 or 10.")


@click.command("lip-sync")
@click.option("--video-id", default=None, help="Kling source video ID.")
@click.option("--video-url", default=None, help="Kling source video URL.")
@click.option(
    "--mode",
    required=True,
    type=click.Choice(["audio2video", "text2video"]),
    help="Lip-sync mode.",
)
@click.option("--audio-url", default=None, help="Audio URL for audio2video mode.")
@click.option(
    "--audio-type",
    type=click.Choice(["url", "file"]),
    default=None,
    help="Audio source type.",
)
@click.option("--audio-file", default=None, help="Path or content string for audio2video mode.")
@click.option("--text", default=None, help="Text for text2video mode.")
@click.option("--voice-id", default=None, help="Voice ID for text2video mode.")
@click.option(
    "--voice-language",
    type=click.Choice(["zh", "en"]),
    default=None,
    help="Voice language for text2video mode.",
)
@click.option(
    "--voice-speed",
    default=None,
    type=float,
    help="Voice speed multiplier for text2video mode (1.0 = normal).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def lip_sync(
    ctx: click.Context,
    video_id: str | None,
    video_url: str | None,
    mode: str,
    audio_url: str | None,
    audio_type: str | None,
    audio_file: str | None,
    text: str | None,
    voice_id: str | None,
    voice_language: str | None,
    voice_speed: float | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a lip-sync video."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.lip_sync(
            video_id=video_id,
            video_url=video_url,
            mode=mode,
            audio_url=audio_url,
            audio_type=audio_type,
            audio_file=audio_file,
            text=text,
            voice_id=voice_id,
            voice_language=voice_language,
            voice_speed=voice_speed,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("talking-photo")
@click.option("--image-url", required=True, help="Source image URL.")
@click.option("--audio-url", required=True, help="Source audio URL.")
@click.option("--prompt", default=None, help="Prompt for talking photo generation.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(TALKING_PHOTO_MODELS),
    default=None,
    help="Model to use for generation.",
)
@click.option(
    "--duration",
    type=int,
    callback=_validate_duration,
    default=None,
    help="Video duration in seconds.",
)
@click.option(
    "--mode",
    type=click.Choice(["std", "pro"]),
    default=None,
    help="Generation mode: std or pro.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def talking_photo(
    ctx: click.Context,
    image_url: str,
    audio_url: str,
    prompt: str | None,
    model: str | None,
    duration: int | None,
    mode: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a talking-photo video."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.talking_photo(
            image_url=image_url,
            audio_url=audio_url,
            prompt=prompt,
            model=model,
            duration=duration,
            mode=mode,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

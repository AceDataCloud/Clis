"""Talking photo command."""

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import (
    print_error,
    print_json,
    print_video_result,
)

TALKING_PHOTO_MODELS = [
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
]

DEFAULT_TALKING_PHOTO_MODEL = "kling-v2-1-master"
DEFAULT_TALKING_PHOTO_MODE = "pro"


@click.command("talking-photo")
@click.option(
    "--image-url",
    required=True,
    help="Public URL of the portrait image (clear frontal face works best).",
)
@click.option(
    "--audio-url",
    required=True,
    help="Public URL of the driving audio (.mp3/.wav/.m4a/.aac, ≤5MB).",
)
@click.option("--prompt", default=None, help="Motion/expression hint for the animation step.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(TALKING_PHOTO_MODELS),
    default=DEFAULT_TALKING_PHOTO_MODEL,
    help="Kling model for the animation step.",
)
@click.option(
    "--duration",
    type=click.Choice(["5", "10"]),
    default="5",
    help="Video length in seconds (5 or 10).",
)
@click.option(
    "--mode",
    type=click.Choice(["std", "pro"]),
    default=DEFAULT_TALKING_PHOTO_MODE,
    help="Animation quality: std (standard) or pro (high quality).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def talking_photo(
    ctx: click.Context,
    image_url: str,
    audio_url: str,
    prompt: str | None,
    model: str,
    duration: str,
    mode: str,
    callback_url: str | None,
    async_mode: bool,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Turn a portrait photo + audio into a talking video.

    Combines image2video animation with lip-sync in a single call.
    Generation takes ~4–6 minutes; consider using --async with 'kling task'.

    Examples:

      kling talking-photo --image-url https://example.com/face.jpg \\
        --audio-url https://example.com/speech.mp3

      kling talking-photo --image-url img.jpg --audio-url audio.mp3 --duration 10 --async
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "image_url": image_url,
            "audio_url": audio_url,
            "model": model,
            "duration": int(duration),
            "mode": mode,
            "callback_url": callback_url,
            "async": async_mode,
            "timeout": timeout,
        }
        if prompt:
            payload["prompt"] = prompt

        result = client.talking_photo(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Video generation commands."""

import click

from wan_cli.core.client import get_client
from wan_cli.core.exceptions import WanError
from wan_cli.core.output import (
    DEFAULT_MODEL,
    DURATIONS,
    RESOLUTIONS,
    SHOT_TYPES,
    WAN_MODELS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(WAN_MODELS),
    default=DEFAULT_MODEL,
    help="Wan model version.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution (480P, 720P, 1080P).",
)
@click.option(
    "--shot-type",
    type=click.Choice(SHOT_TYPES),
    default=None,
    help="Shot type: single continuous shot or multi switching shots.",
)
@click.option(
    "--duration",
    type=click.Choice([str(d) for d in DURATIONS]),
    default=None,
    help="Duration in seconds (5, 10, 15).",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Reverse prompt words describing content to exclude from the video.",
)
@click.option(
    "--size",
    default=None,
    help="The size of the generated video.",
)
@click.option(
    "--audio/--no-audio",
    default=None,
    help="Whether the generated video has sound.",
)
@click.option(
    "--prompt-extend/--no-prompt-extend",
    default=None,
    help="Enable prompt intelligent rewriting.",
)
@click.option(
    "--audio-url",
    default=None,
    help="URL of an audio file to use in the generated video.",
)
@click.option(
    "--reference-video-urls",
    multiple=True,
    help="Reference video URL for character/timbre extraction (repeatable). Used with the wan2.6-r2v model.",
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
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    resolution: str | None,
    shot_type: str | None,
    duration: str | None,
    negative_prompt: str | None,
    size: str | None,
    audio: bool | None,
    prompt_extend: bool | None,
    audio_url: str | None,
    reference_video_urls: tuple[str, ...],
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      wan generate "Astronauts shuttle from space to volcano"

      wan generate "A cat playing with yarn" -m wan2.6-t2v

      wan generate "Transform this scene" -m wan2.6-r2v --reference-video-urls https://example.com/ref.mp4
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "text2video",
            "prompt": prompt,
            "model": model,
            "resolution": resolution,
            "shot_type": shot_type,
            "duration": int(duration) if duration is not None else None,
            "negative_prompt": negative_prompt,
            "size": size,
            "audio": audio,
            "prompt_extend": prompt_extend,
            "audio_url": audio_url,
            "reference_video_urls": list(reference_video_urls) if reference_video_urls else None,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except WanError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    required=True,
    help="URL of the start image (first frame of the generated video).",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(WAN_MODELS),
    default="wan2.6-i2v",
    help="Wan model version.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution (480P, 720P, 1080P).",
)
@click.option(
    "--shot-type",
    type=click.Choice(SHOT_TYPES),
    default=None,
    help="Shot type: single continuous shot or multi switching shots.",
)
@click.option(
    "--duration",
    type=click.Choice([str(d) for d in DURATIONS]),
    default=None,
    help="Duration in seconds (5, 10, 15).",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Reverse prompt words describing content to exclude from the video.",
)
@click.option(
    "--size",
    default=None,
    help="The size of the generated video.",
)
@click.option(
    "--audio/--no-audio",
    default=None,
    help="Whether the generated video has sound.",
)
@click.option(
    "--prompt-extend/--no-prompt-extend",
    default=None,
    help="Enable prompt intelligent rewriting.",
)
@click.option(
    "--audio-url",
    default=None,
    help="URL of an audio file to use in the generated video.",
)
@click.option(
    "--reference-video-urls",
    multiple=True,
    help="Reference video URL for character/timbre extraction (repeatable).",
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
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_url: str,
    model: str,
    resolution: str | None,
    shot_type: str | None,
    duration: str | None,
    negative_prompt: str | None,
    size: str | None,
    audio: bool | None,
    prompt_extend: bool | None,
    audio_url: str | None,
    reference_video_urls: tuple[str, ...],
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from a reference image.

    PROMPT describes the desired video. Provide an image URL as the first frame.

    Examples:

      wan image-to-video "Animate this scene" -i https://example.com/photo.jpg

      wan image-to-video "Bring to life" -i https://cdn.acedata.cloud/r9vsv9.png -m wan2.6-i2v
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "image2video",
            "prompt": prompt,
            "model": model,
            "image_url": image_url,
            "resolution": resolution,
            "shot_type": shot_type,
            "duration": int(duration) if duration is not None else None,
            "negative_prompt": negative_prompt,
            "size": size,
            "audio": audio,
            "prompt_extend": prompt_extend,
            "audio_url": audio_url,
            "reference_video_urls": list(reference_video_urls) if reference_video_urls else None,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except WanError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("wan3")
@click.argument("prompt", required=False, default="")
@click.option("--media", "media_items", multiple=True, help="Repeatable TYPE=URL media item.")
@click.option("--duration", type=click.IntRange(-1, 30), default=5)
@click.option("--resolution", type=click.Choice(["480P", "720P", "1080P"]), default="1080P")
@click.option(
    "--ratio",
    type=click.Choice(["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16"]),
    default="adaptive",
)
@click.option("--audio/--no-audio", default=True)
@click.option("--seed", type=click.IntRange(0, 2147483647), default=None)
@click.option("--watermark/--no-watermark", default=False)
@click.option("--callback-url", default=None)
@click.option("--async", "async_mode", is_flag=True)
@click.option("--json", "output_json", is_flag=True)
@click.pass_context
def wan3(
    ctx: click.Context,
    prompt: str,
    media_items: tuple[str, ...],
    duration: int,
    resolution: str,
    ratio: str,
    audio: bool,
    seed: int | None,
    watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a Wan 3 video from text and optional reference media."""
    if duration in (0, 1):
        raise click.BadParameter("duration must be -1 or 2-30")
    media = []
    for item in media_items:
        if "=" not in item:
            raise click.BadParameter("media must use TYPE=URL")
        kind, url = item.split("=", 1)
        media.append({"type": kind, "url": url})
    if not prompt and not media:
        raise click.BadParameter("prompt or media is required")
    payload = {
        "model": "wan3.0-video",
        "prompt": prompt,
        "media": media or None,
        "duration": duration,
        "resolution": resolution,
        "ratio": ratio,
        "audio": audio,
        "seed": seed,
        "watermark": watermark,
        "callback_url": callback_url,
        "async": async_mode,
    }
    try:
        result = get_client(ctx.obj.get("token")).generate_video(**payload)
        (print_json if output_json else print_video_result)(result)
    except WanError as e:
        print_error(e.message)
        raise SystemExit(1) from e

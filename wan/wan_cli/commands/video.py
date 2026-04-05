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
    "-d",
    "--duration",
    type=click.Choice([str(d) for d in DURATIONS]),
    default=None,
    help="Video duration in seconds (5, 10, 15).",
)
@click.option(
    "--shot-type",
    type=click.Choice(SHOT_TYPES),
    default=None,
    help="Shot type: single continuous shot or multi switching shots.",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Content to exclude from the generated video.",
)
@click.option(
    "--size",
    default=None,
    help="Size of the generated video.",
)
@click.option(
    "--audio/--no-audio",
    default=None,
    help="Whether the generated video has sound.",
)
@click.option(
    "--prompt-extend/--no-prompt-extend",
    default=None,
    help="Enable intelligent prompt rewriting for better results.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    resolution: str | None,
    duration: str | None,
    shot_type: str | None,
    negative_prompt: str | None,
    size: str | None,
    audio: bool | None,
    prompt_extend: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      wan generate "Astronauts shuttle from space to volcano"

      wan generate "A cat playing in the garden" -m wan2.6-t2v -r 720P
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "text2video",
            "prompt": prompt,
            "model": model,
            "resolution": resolution,
            "duration": int(duration) if duration is not None else None,
            "shot_type": shot_type,
            "negative_prompt": negative_prompt,
            "size": size,
            "audio": audio,
            "prompt_extend": prompt_extend,
            "callback_url": callback_url,
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
    help="URL of the start image (first frame of the video).",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(["wan2.6-i2v", "wan2.6-i2v-flash"]),
    default="wan2.6-i2v",
    help="Wan image-to-video model.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution (480P, 720P, 1080P).",
)
@click.option(
    "-d",
    "--duration",
    type=click.Choice([str(d) for d in DURATIONS]),
    default=None,
    help="Video duration in seconds (5, 10, 15).",
)
@click.option(
    "--shot-type",
    type=click.Choice(SHOT_TYPES),
    default=None,
    help="Shot type: single continuous shot or multi switching shots.",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Content to exclude from the generated video.",
)
@click.option(
    "--audio/--no-audio",
    default=None,
    help="Whether the generated video has sound.",
)
@click.option(
    "--prompt-extend/--no-prompt-extend",
    default=None,
    help="Enable intelligent prompt rewriting for better results.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_url: str,
    model: str,
    resolution: str | None,
    duration: str | None,
    shot_type: str | None,
    negative_prompt: str | None,
    audio: bool | None,
    prompt_extend: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a reference image.

    PROMPT describes the desired video motion. Provide an image URL as the starting frame.

    Examples:

      wan image-to-video "Animate this scene" -i https://example.com/photo.jpg

      wan image-to-video "Bring to life" -i https://cdn.acedata.cloud/r9vsv9.png -m wan2.6-i2v
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            action="image2video",
            prompt=prompt,
            image_url=image_url,
            model=model,
            resolution=resolution,
            duration=int(duration) if duration is not None else None,
            shot_type=shot_type,
            negative_prompt=negative_prompt,
            audio=audio,
            prompt_extend=prompt_extend,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except WanError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("reference-to-video")
@click.argument("prompt")
@click.option(
    "--reference-video-urls",
    required=True,
    help="URL(s) of reference video file(s) to extract character/timbre features from.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(["wan2.6-r2v"]),
    default="wan2.6-r2v",
    help="Wan reference-to-video model.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution (480P, 720P, 1080P).",
)
@click.option(
    "-d",
    "--duration",
    type=click.Choice([str(d) for d in DURATIONS]),
    default=None,
    help="Video duration in seconds (5, 10, 15).",
)
@click.option(
    "--audio-url",
    default=None,
    help="URL of an audio file to use in the generated video.",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Content to exclude from the generated video.",
)
@click.option(
    "--audio/--no-audio",
    default=None,
    help="Whether the generated video has sound.",
)
@click.option(
    "--prompt-extend/--no-prompt-extend",
    default=None,
    help="Enable intelligent prompt rewriting for better results.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def reference_to_video(
    ctx: click.Context,
    prompt: str,
    reference_video_urls: str,
    model: str,
    resolution: str | None,
    duration: str | None,
    audio_url: str | None,
    negative_prompt: str | None,
    audio: bool | None,
    prompt_extend: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video using a reference video for character/timbre features.

    PROMPT describes the desired video. Provide a reference video URL to extract features from.

    Examples:

      wan reference-to-video "A person dancing" --reference-video-urls https://example.com/ref.mp4
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            action="text2video",
            prompt=prompt,
            reference_video_urls=reference_video_urls,
            model=model,
            resolution=resolution,
            duration=int(duration) if duration is not None else None,
            audio_url=audio_url,
            negative_prompt=negative_prompt,
            audio=audio,
            prompt_extend=prompt_extend,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except WanError as e:
        print_error(e.message)
        raise SystemExit(1) from e

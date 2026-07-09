"""Video generation commands."""

import click

from happyhorse_cli.core.client import get_client
from happyhorse_cli.core.exceptions import HappyHorseError
from happyhorse_cli.core.output import (
    DEFAULT_MODEL,
    HAPPYHORSE_MODELS,
    print_error,
    print_json,
    print_video_result,
)

TEXT_TO_VIDEO_MODELS = ["happyhorse-1.0-t2v", "happyhorse-1.1-t2v"]
IMAGE_TO_VIDEO_MODELS = ["happyhorse-1.0-i2v", "happyhorse-1.1-i2v"]
REFERENCE_TO_VIDEO_MODELS = ["happyhorse-1.0-r2v", "happyhorse-1.1-r2v"]
VIDEO_EDIT_MODELS = ["happyhorse-1.0-video-edit"]

RESOLUTION_CHOICES = ["720P", "1080P"]
RATIO_CHOICES = ["16:9", "9:16", "1:1", "4:3", "3:4"]
AUDIO_SETTING_CHOICES = ["auto", "origin"]


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(HAPPYHORSE_MODELS),
    default=DEFAULT_MODEL,
    help="HappyHorse model to use (default: happyhorse-1.1-t2v).",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="1080P",
    help="Video resolution (default: 1080P).",
)
@click.option(
    "--ratio",
    type=click.Choice(RATIO_CHOICES),
    default="16:9",
    help="Video aspect ratio (default: 16:9).",
)
@click.option("--duration", type=int, default=5, help="Video duration in seconds (default: 5).")
@click.option(
    "--watermark/--no-watermark",
    default=False,
    help="Add watermark to the video (default: no watermark).",
)
@click.option(
    "--audio-setting",
    type=click.Choice(AUDIO_SETTING_CHOICES),
    default="auto",
    help="Audio setting (default: auto).",
)
@click.option("--seed", type=int, default=None, help="Random seed for reproducibility.")
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
    resolution: str,
    ratio: str,
    duration: int,
    watermark: bool,
    audio_setting: str,
    seed: int | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    \b
    Examples:
      happyhorse generate "A horse galloping through a field"
      happyhorse generate "Sunset over mountains" --resolution 720P --ratio 9:16
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "model": model,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "watermark": watermark,
            "audio_setting": audio_setting,
            "seed": seed,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HappyHorseError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option("--image-url", required=True, help="URL of the reference image.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(IMAGE_TO_VIDEO_MODELS),
    default="happyhorse-1.1-i2v",
    help="HappyHorse image-to-video model (default: happyhorse-1.1-i2v).",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="1080P",
    help="Video resolution (default: 1080P).",
)
@click.option(
    "--ratio",
    type=click.Choice(RATIO_CHOICES),
    default="16:9",
    help="Video aspect ratio (default: 16:9).",
)
@click.option("--duration", type=int, default=5, help="Video duration in seconds (default: 5).")
@click.option(
    "--watermark/--no-watermark",
    default=False,
    help="Add watermark to the video (default: no watermark).",
)
@click.option(
    "--audio-setting",
    type=click.Choice(AUDIO_SETTING_CHOICES),
    default="auto",
    help="Audio setting (default: auto).",
)
@click.option("--seed", type=int, default=None, help="Random seed for reproducibility.")
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
    resolution: str,
    ratio: str,
    duration: int,
    watermark: bool,
    audio_setting: str,
    seed: int | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from an image and text prompt.

    PROMPT describes the desired video content.

    \b
    Examples:
      happyhorse image-to-video "Animate this scene" --image-url https://example.com/photo.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "image_to_video",
            "prompt": prompt,
            "model": model,
            "image_url": image_url,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "watermark": watermark,
            "audio_setting": audio_setting,
            "seed": seed,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HappyHorseError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("reference-to-video")
@click.argument("prompt")
@click.option(
    "--image-urls",
    required=True,
    multiple=True,
    help="URLs of reference images (can be specified multiple times).",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(REFERENCE_TO_VIDEO_MODELS),
    default="happyhorse-1.1-r2v",
    help="HappyHorse reference-to-video model (default: happyhorse-1.1-r2v).",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="1080P",
    help="Video resolution (default: 1080P).",
)
@click.option(
    "--ratio",
    type=click.Choice(RATIO_CHOICES),
    default="16:9",
    help="Video aspect ratio (default: 16:9).",
)
@click.option("--duration", type=int, default=5, help="Video duration in seconds (default: 5).")
@click.option(
    "--watermark/--no-watermark",
    default=False,
    help="Add watermark to the video (default: no watermark).",
)
@click.option(
    "--audio-setting",
    type=click.Choice(AUDIO_SETTING_CHOICES),
    default="auto",
    help="Audio setting (default: auto).",
)
@click.option("--seed", type=int, default=None, help="Random seed for reproducibility.")
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
def reference_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    resolution: str,
    ratio: str,
    duration: int,
    watermark: bool,
    audio_setting: str,
    seed: int | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from reference images and text prompt.

    PROMPT describes the desired video content.

    \b
    Examples:
      happyhorse reference-to-video "Create scene" --image-urls https://example.com/ref1.jpg
      happyhorse reference-to-video "Combine scenes" \\
          --image-urls https://example.com/ref1.jpg \\
          --image-urls https://example.com/ref2.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "reference_to_video",
            "prompt": prompt,
            "model": model,
            "image_urls": list(image_urls),
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "watermark": watermark,
            "audio_setting": audio_setting,
            "seed": seed,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HappyHorseError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("video-edit")
@click.argument("prompt")
@click.option("--video-url", required=True, help="URL of the source video to edit.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(VIDEO_EDIT_MODELS),
    default="happyhorse-1.0-video-edit",
    help="HappyHorse video-edit model (default: happyhorse-1.0-video-edit).",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="1080P",
    help="Video resolution (default: 1080P).",
)
@click.option(
    "--ratio",
    type=click.Choice(RATIO_CHOICES),
    default="16:9",
    help="Video aspect ratio (default: 16:9).",
)
@click.option("--duration", type=int, default=5, help="Video duration in seconds (default: 5).")
@click.option(
    "--watermark/--no-watermark",
    default=False,
    help="Add watermark to the video (default: no watermark).",
)
@click.option(
    "--audio-setting",
    type=click.Choice(AUDIO_SETTING_CHOICES),
    default="auto",
    help="Audio setting (default: auto).",
)
@click.option("--seed", type=int, default=None, help="Random seed for reproducibility.")
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
def video_edit(
    ctx: click.Context,
    prompt: str,
    video_url: str,
    model: str,
    resolution: str,
    ratio: str,
    duration: int,
    watermark: bool,
    audio_setting: str,
    seed: int | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Edit a video using text instructions.

    PROMPT describes the desired edits to the video.

    \b
    Examples:
      happyhorse video-edit "Add dramatic music" --video-url https://example.com/video.mp4
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "video_edit",
            "prompt": prompt,
            "model": model,
            "video_url": video_url,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "watermark": watermark,
            "audio_setting": audio_setting,
            "seed": seed,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HappyHorseError as e:
        print_error(e.message)
        raise SystemExit(1) from e

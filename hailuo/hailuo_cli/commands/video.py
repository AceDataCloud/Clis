"""Video generation commands."""

import click

from hailuo_cli.core.client import get_client
from hailuo_cli.core.exceptions import HailuoError
from hailuo_cli.core.output import (
    DEFAULT_MODEL,
    HAILUO_MODELS,
    print_error,
    print_json,
    print_video_result,
)

RESOLUTION_CHOICES = ["768P", "2K"]


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "-m",
    "--model",
    type=click.Choice(HAILUO_MODELS),
    default=DEFAULT_MODEL,
    help="Hailuo model to use (default: minimax-h3).",
)
@click.option(
    "--image-url",
    "image_urls",
    multiple=True,
    help="Image URL input (repeat up to 9 times).",
)
@click.option(
    "--audio-url",
    "audio_urls",
    multiple=True,
    help="Audio URL input (repeat up to 3 times).",
)
@click.option(
    "--ratio",
    type=click.Choice(["16:9", "9:16"]),
    default="16:9",
    show_default=True,
    help="Output aspect ratio.",
)
@click.option(
    "--duration",
    type=click.IntRange(4, 15),
    default=4,
    show_default=True,
    help="Output duration in seconds.",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="2K",
    show_default=True,
    help="Output resolution.",
)
@click.option(
    "--aigc-watermark/--no-aigc-watermark",
    default=False,
    show_default=True,
    help="Whether to enable AIGC watermark.",
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
    prompt: str | None,
    model: str,
    image_urls: tuple[str, ...],
    audio_urls: tuple[str, ...],
    ratio: str,
    duration: int,
    resolution: str,
    aigc_watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    \b
    Examples:
      hailuo generate "A cat playing in the snow"
      hailuo generate "Ocean waves at sunset" --model minimax-h3
    """
    client = get_client(ctx.obj.get("token"))
    try:
        if not prompt and not image_urls and not audio_urls:
            raise click.UsageError(
                "Provide PROMPT or at least one --image-url or --audio-url input."
            )
        if len(image_urls) > 9:
            raise click.UsageError("You can provide at most 9 --image-url values.")
        if len(audio_urls) > 3:
            raise click.UsageError("You can provide at most 3 --audio-url values.")

        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "image_urls": list(image_urls) or None,
            "audio_urls": list(audio_urls) or None,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "aigc_watermark": aigc_watermark,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HailuoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option("--image-url", required=True, help="URL of the first frame reference image.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(HAILUO_MODELS),
    default=DEFAULT_MODEL,
    help="Hailuo image-to-video model (default: minimax-h3).",
)
@click.option(
    "--ratio",
    type=click.Choice(["16:9", "9:16"]),
    default="16:9",
    show_default=True,
    help="Output aspect ratio.",
)
@click.option(
    "--duration",
    type=click.IntRange(4, 15),
    default=4,
    show_default=True,
    help="Output duration in seconds.",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="2K",
    show_default=True,
    help="Output resolution.",
)
@click.option(
    "--aigc-watermark/--no-aigc-watermark",
    default=False,
    show_default=True,
    help="Whether to enable AIGC watermark.",
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
    ratio: str,
    duration: int,
    resolution: str,
    aigc_watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from an image and text prompt.

    PROMPT describes the desired video content.

    \b
    Examples:
      hailuo image-to-video "Animate this scene" --image-url https://example.com/photo.jpg
      hailuo image-to-video "Cinematic pan" --image-url img.jpg --model minimax-h3
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "image_urls": [image_url],
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "aigc_watermark": aigc_watermark,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HailuoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

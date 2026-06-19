"""Video generation command."""

import click

from grok_cli.core.client import get_client
from grok_cli.core.exceptions import GrokError
from grok_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_RESOLUTION,
    DEFAULT_VIDEO_MODEL,
    GROK_VIDEO_MODELS,
    RESOLUTIONS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt", required=False, default=None)
@click.option(
    "-m",
    "--model",
    type=click.Choice(GROK_VIDEO_MODELS),
    default=DEFAULT_VIDEO_MODEL,
    show_default=True,
    help="Grok video model to use.",
)
@click.option(
    "--image-url",
    default=None,
    help="URL of the reference image for image-to-video generation.",
)
@click.option(
    "--reference-image-url",
    multiple=True,
    default=None,
    help="URL(s) of reference image(s) (repeatable).",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=None,
    help="Aspect ratio of the output video.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=DEFAULT_RESOLUTION,
    show_default=True,
    help="Output resolution.",
)
@click.option(
    "--duration",
    type=int,
    default=None,
    help="Duration of the video in seconds.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Webhook callback URL.",
)
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def video(
    ctx: click.Context,
    prompt: str | None,
    model: str,
    image_url: str | None,
    reference_image_url: tuple[str, ...],
    aspect_ratio: str | None,
    resolution: str,
    duration: int | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video using Grok.

    PROMPT is an optional text description of the video to generate.

    \b
    Examples:
      grok video "A sunset over the ocean"
      grok video "Animate this scene" --image-url https://example.com/photo.jpg
      grok video "Cinematic landscape" --aspect-ratio 16:9 --resolution 720p --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "model": model,
        "resolution": resolution,
    }
    if prompt is not None:
        payload["prompt"] = prompt
    if image_url is not None:
        payload["image_url"] = image_url
    if reference_image_url:
        payload["reference_image_urls"] = list(reference_image_url)
    if aspect_ratio is not None:
        payload["aspect_ratio"] = aspect_ratio
    if duration is not None:
        payload["duration"] = duration
    if callback_url is not None:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate_video(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except GrokError as e:
        print_error(e.message)
        raise SystemExit(1) from e

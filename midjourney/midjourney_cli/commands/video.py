"""Video generation commands."""

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import (
    DEFAULT_VIDEO_MODE,
    VIDEO_MODES,
    VIDEO_RESOLUTIONS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option("--image-url", required=True, help="URL of the first frame reference image.")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(VIDEO_MODES),
    default=DEFAULT_VIDEO_MODE,
    help="Generation mode (fast or turbo).",
)
@click.option(
    "--resolution",
    type=click.Choice(VIDEO_RESOLUTIONS),
    default="720p",
    help="Video resolution.",
)
@click.option("--end-image-url", default=None, help="URL of the last frame reference image.")
@click.option("--loop", is_flag=True, default=False, help="Generate a looping video.")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def video(
    ctx: click.Context,
    prompt: str,
    image_url: str,
    mode: str,
    resolution: str,
    end_image_url: str | None,
    loop: bool,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from text prompt and reference image.

    PROMPT describes the desired video content.

    \b
    Examples:
      midjourney video "A cat walking" --image-url https://example.com/cat.jpg
      midjourney video "Ocean waves" --image-url img.jpg --resolution 720p --loop
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "image_url": image_url,
            "mode": mode,
            "resolution": resolution,
            "loop": loop,
            "callback_url": callback_url,
            "end_image_url": end_image_url,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("extend-video")
@click.argument("video_id")
@click.argument("prompt")
@click.option(
    "--video-index",
    type=int,
    default=0,
    help="Index of the video to extend from video_urls (0-indexed).",
)
@click.option(
    "-m",
    "--mode",
    type=click.Choice(VIDEO_MODES),
    default=DEFAULT_VIDEO_MODE,
    help="Generation mode.",
)
@click.option("--end-image-url", default=None, help="URL of the final frame image.")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def extend_video(
    ctx: click.Context,
    video_id: str,
    prompt: str,
    video_index: int,
    mode: str,
    end_image_url: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Extend an existing video to make it longer.

    VIDEO_ID is the video_id from a previous video generation.
    PROMPT describes how the video should continue.

    \b
    Examples:
      midjourney extend-video vid-123 "Continue the action"
      midjourney extend-video vid-123 "Zoom into the scene" --video-index 1
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "extend",
            "video_id": video_id,
            "video_index": video_index,
            "prompt": prompt,
            "mode": mode,
            "callback_url": callback_url,
            "end_image_url": end_image_url,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Video generation commands."""

import click

from luma_cli.core.client import get_client
from luma_cli.core.exceptions import LumaError
from luma_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ASPECT_RATIO,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option("--loop", is_flag=True, default=False, help="Enable loop for the generated video.")
@click.option(
    "--enhancement/--no-enhancement",
    default=True,
    help="Enable prompt text enhancement (default: enabled).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    aspect_ratio: str,
    loop: bool,
    enhancement: bool,
    callback_url: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      luma generate "A cinematic scene of a sunset over the ocean"

      luma generate "A cat playing with yarn" --loop
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "loop": loop,
            "enhancement": enhancement,
            "callback_url": callback_url,
            "timeout": timeout,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except LumaError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option(
    "--start-image-url",
    default=None,
    help="URL of the start image (first frame of the video).",
)
@click.option(
    "--end-image-url",
    default=None,
    help="URL of the end image (last frame of the video).",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option("--loop", is_flag=True, default=False, help="Enable loop for the generated video.")
@click.option(
    "--enhancement/--no-enhancement",
    default=True,
    help="Enable prompt text enhancement (default: enabled).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    start_image_url: str | None,
    end_image_url: str | None,
    aspect_ratio: str,
    loop: bool,
    enhancement: bool,
    callback_url: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s).

    PROMPT describes the desired video. Provide a start and/or end image URL.

    Examples:

      luma image-to-video "Animate this scene" --start-image-url https://example.com/photo.jpg

      luma image-to-video "Transition" --start-image-url img1.jpg --end-image-url img2.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            action="generate",
            prompt=prompt,
            start_image_url=start_image_url,
            end_image_url=end_image_url,
            aspect_ratio=aspect_ratio,
            loop=loop,
            enhancement=enhancement,
            callback_url=callback_url,
            timeout=timeout,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except LumaError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("video_id", required=False, default=None)
@click.option("--video-url", default=None, help="URL of the video to extend.")
@click.option("--prompt", default=None, help="Prompt for extension direction.")
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def extend(
    ctx: click.Context,
    video_id: str | None,
    video_url: str | None,
    prompt: str | None,
    aspect_ratio: str,
    callback_url: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Extend an existing video.

    VIDEO_ID is the ID of the video to extend. Use --video-url to extend by URL instead.

    Examples:

      luma extend abc123-def456

      luma extend abc123 --prompt "Continue the action"

      luma extend --video-url https://example.com/video.mp4
    """
    if not video_id and not video_url:
        raise click.UsageError("Provide VIDEO_ID or --video-url.")
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.extend_video(
            action="extend",
            video_id=video_id,
            video_url=video_url,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            callback_url=callback_url,
            timeout=timeout,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except LumaError as e:
        print_error(e.message)
        raise SystemExit(1) from e

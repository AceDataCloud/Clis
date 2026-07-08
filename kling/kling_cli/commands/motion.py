"""Motion generation command."""

import json

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import (
    DEFAULT_MODE,
    KLING_MODES,
    print_error,
    print_json,
    print_video_result,
)

MOTION_MODELS = ["kling-v2-6", "kling-v3"]


@click.command()
@click.option(
    "--image-url",
    required=True,
    help="Reference image URL. Characters, backgrounds and elements in the generated video "
    "are based on this image.",
)
@click.option(
    "--video-url",
    required=True,
    help="Reference video URL. Character movements in the generated video are consistent "
    "with those in this reference video.",
)
@click.option(
    "--character-orientation",
    default=None,
    type=click.Choice(["image", "video"]),
    help="Orientation of characters in the generated video: consistent with the image or video.",
)
@click.option(
    "--mode",
    type=click.Choice(KLING_MODES),
    default=DEFAULT_MODE,
    help="Generation mode: std (High performance) or pro (High quality).",
)
@click.option(
    "-m",
    "--model-name",
    type=click.Choice(MOTION_MODELS),
    default=None,
    help="Model to use for motion generation.",
)
@click.option(
    "--keep-original-sound/--no-keep-original-sound",
    default=True,
    help="Whether to keep the original sound from the reference video (default: keep).",
)
@click.option(
    "--watermark-info",
    default=None,
    help='Watermark configuration as a JSON string, e.g. \'{"enabled": true}\'.',
)
@click.option("--prompt", default=None, help="Text prompt (positive and/or negative descriptions).")
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
def motion(
    ctx: click.Context,
    image_url: str,
    video_url: str,
    character_orientation: str | None,
    mode: str,
    model_name: str | None,
    keep_original_sound: bool,
    watermark_info: str | None,
    prompt: str | None,
    callback_url: str | None,
    async_mode: bool,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Generate a motion video from a reference image and reference video.

    The generated video's characters and elements are based on the reference image,
    while the movements are based on the reference video.

    Examples:

      kling motion --image-url https://example.com/img.jpg --video-url https://example.com/ref.mp4

      kling motion --image-url img.jpg --video-url ref.mp4 --prompt "A dancer performing"
    """
    parsed_watermark_info = None
    if watermark_info is not None:
        try:
            parsed_watermark_info = json.loads(watermark_info)
        except json.JSONDecodeError as exc:
            raise click.BadParameter(
                "Must be a valid JSON string.", param_hint="--watermark-info"
            ) from exc

    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_motion(
            image_url=image_url,
            video_url=video_url,
            character_orientation=character_orientation,
            mode=mode,
            model_name=model_name,
            keep_original_sound="yes" if keep_original_sound else "no",
            watermark_info=parsed_watermark_info,
            prompt=prompt,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
            timeout=timeout,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

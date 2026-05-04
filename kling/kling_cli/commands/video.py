"""Video generation commands."""

import json
from typing import Any

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_MODE,
    DEFAULT_MODEL,
    KLING_MODELS,
    KLING_MODES,
    print_error,
    print_json,
    print_video_result,
)


def _parse_json_option(value: str | None, param_hint: str) -> Any:
    """Parse a JSON string option, raising BadParameter on invalid JSON."""
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter("Must be a valid JSON string.", param_hint=param_hint) from exc


def _build_element_list(element_ids: tuple[str, ...]) -> list[dict[str, str]] | None:
    """Build an element_list payload from a tuple of element IDs."""
    return [{"element_id": eid} for eid in element_ids] if element_ids else None


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(KLING_MODELS),
    default=DEFAULT_MODEL,
    help="Model to use for generation.",
)
@click.option(
    "--mode",
    type=click.Choice(KLING_MODES),
    default=DEFAULT_MODE,
    help="Generation mode: std (High performance), pro (High quality), 4k (Native 4K).",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option(
    "--duration",
    default=None,
    type=int,
    help="Video duration in seconds (5 or 10 for most models; 3-15 for kling-v3/kling-v3-omni).",
)
@click.option(
    "--cfg-scale",
    default=None,
    type=float,
    help="Degree of freedom to generate video [0,1]. Higher = stronger correlation.",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Negative prompt (max 200 characters).",
)
@click.option(
    "--generate-audio/--no-generate-audio",
    default=None,
    help="Generate audio along with the video (supported by kling-v3, kling-v3-omni, kling-v2-6 pro).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--camera-control",
    default=None,
    help=(
        "Camera movement control as a JSON string. "
        "Keys: type (one of simple/down_back/forward_up/left_turn_forward/right_turn_forward) "
        "and optional config object with fields horizontal/vertical/pan/tilt/roll/zoom [-1,1]. "
        'Example: \'{"type": "simple", "config": {"horizontal": 0.5}}\''
    ),
)
@click.option(
    "--element-id",
    "element_ids",
    multiple=True,
    help=(
        "Reference subject ID from the subject library. "
        "Can be specified multiple times (max 7 without reference video, 4 with)."
    ),
)
@click.option(
    "--video-list",
    default=None,
    help=(
        "Reference video(s) as a JSON array string. Each item must have video_url and may "
        "include refer_type (feature or base) and keep_original_sound (yes/no). "
        'Example: \'[{"video_url": "https://...", "refer_type": "base"}]\''
    ),
)
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    mode: str,
    aspect_ratio: str,
    duration: int | None,
    cfg_scale: float | None,
    negative_prompt: str | None,
    generate_audio: bool | None,
    callback_url: str | None,
    camera_control: str | None,
    element_ids: tuple[str, ...],
    video_list: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt (text2video).

    PROMPT is a detailed description of what to generate.

    Examples:

      kling generate "A cinematic scene of a sunset over the ocean"

      kling generate "A cat playing with yarn" --model kling-v3 --mode 4k
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "text2video",
            "prompt": prompt,
            "model": model,
            "mode": mode,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "cfg_scale": cfg_scale,
            "negative_prompt": negative_prompt,
            "generate_audio": generate_audio,
            "callback_url": callback_url,
            "camera_control": _parse_json_option(camera_control, "--camera-control"),
            "element_list": _build_element_list(element_ids),
            "video_list": _parse_json_option(video_list, "--video-list"),
            "timeout": timeout,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
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
    help="URL of the end image (last frame). Only valid with a non-empty start-image-url.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(KLING_MODELS),
    default=DEFAULT_MODEL,
    help="Model to use for generation.",
)
@click.option(
    "--mode",
    type=click.Choice(KLING_MODES),
    default=DEFAULT_MODE,
    help="Generation mode: std (High performance), pro (High quality), 4k (Native 4K).",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option(
    "--duration",
    default=None,
    type=int,
    help="Video duration in seconds.",
)
@click.option(
    "--cfg-scale",
    default=None,
    type=float,
    help="Degree of freedom to generate video [0,1].",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Negative prompt (max 200 characters).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--camera-control",
    default=None,
    help=(
        "Camera movement control as a JSON string. "
        "Keys: type (one of simple/down_back/forward_up/left_turn_forward/right_turn_forward) "
        "and optional config object with fields horizontal/vertical/pan/tilt/roll/zoom [-1,1]. "
        'Example: \'{"type": "simple", "config": {"horizontal": 0.5}}\''
    ),
)
@click.option(
    "--element-id",
    "element_ids",
    multiple=True,
    help=(
        "Reference subject ID from the subject library. "
        "Can be specified multiple times (max 7 without reference video, 4 with)."
    ),
)
@click.option(
    "--video-list",
    default=None,
    help=(
        "Reference video(s) as a JSON array string. Each item must have video_url and may "
        "include refer_type (feature or base) and keep_original_sound (yes/no). "
        'Example: \'[{"video_url": "https://...", "refer_type": "base"}]\''
    ),
)
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
    model: str,
    mode: str,
    aspect_ratio: str,
    duration: int | None,
    cfg_scale: float | None,
    negative_prompt: str | None,
    callback_url: str | None,
    camera_control: str | None,
    element_ids: tuple[str, ...],
    video_list: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s) (image2video).

    PROMPT describes the desired video. Provide a start and/or end image URL.

    Examples:

      kling image-to-video "Animate this scene" --start-image-url https://example.com/photo.jpg

      kling image-to-video "Transition" --start-image-url img1.jpg --end-image-url img2.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            action="image2video",
            prompt=prompt,
            start_image_url=start_image_url,
            end_image_url=end_image_url,
            model=model,
            mode=mode,
            aspect_ratio=aspect_ratio,
            duration=duration,
            cfg_scale=cfg_scale,
            negative_prompt=negative_prompt,
            callback_url=callback_url,
            camera_control=_parse_json_option(camera_control, "--camera-control"),
            element_list=_build_element_list(element_ids),
            video_list=_parse_json_option(video_list, "--video-list"),
            timeout=timeout,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.option("--video-id", default=None, help="ID of the video to extend.")
@click.option("--prompt", default=None, help="Prompt for extension direction.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(KLING_MODELS),
    default=DEFAULT_MODEL,
    help="Model to use for generation.",
)
@click.option(
    "--mode",
    type=click.Choice(KLING_MODES),
    default=DEFAULT_MODE,
    help="Generation mode: std, pro, or 4k.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio.",
)
@click.option(
    "--duration",
    default=None,
    type=int,
    help="Video duration in seconds.",
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
    prompt: str | None,
    model: str,
    mode: str,
    aspect_ratio: str,
    duration: int | None,
    callback_url: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Extend an existing video.

    Use --video-id to specify the video to extend.

    Examples:

      kling extend --video-id abc123

      kling extend --video-id abc123 --prompt "Continue the action"
    """
    if not video_id:
        raise click.UsageError("Provide --video-id.")
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            action="extend",
            video_id=video_id,
            prompt=prompt,
            model=model,
            mode=mode,
            aspect_ratio=aspect_ratio,
            duration=duration,
            callback_url=callback_url,
            timeout=timeout,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

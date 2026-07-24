"""Video generation commands for Kickart CLI."""

import json

import click

from kickart_cli.core.client import get_client
from kickart_cli.core.exceptions import KickartError
from kickart_cli.core.output import (
    ASPECT_RATIOS,
    LANGUAGES,
    SIMILARITY_LEVELS,
    VIDEO_DURATIONS,
    VIDEO_MODES,
    VIDEO_TYPES,
    VIRAL_MODES,
    print_error,
    print_json,
    print_video_result,
)


def _parse_json_array_option(value: str | None, option_name: str) -> list[object] | None:
    """Parse a JSON array option."""
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be valid JSON.") from exc
    if not isinstance(parsed, list):
        raise click.BadParameter(f"{option_name} must be a JSON array.")
    return parsed


@click.command()
@click.option(
    "--duration",
    required=True,
    type=click.Choice([str(d) for d in VIDEO_DURATIONS]),
    help="Duration of the video in seconds (15, 30, 45, or 60).",
)
@click.option(
    "--mode",
    type=click.Choice(VIDEO_MODES),
    default="fast",
    show_default=True,
    help="Generation mode: fast or pro.",
)
@click.option(
    "--type",
    "video_type",
    type=click.Choice(VIDEO_TYPES),
    default="intro",
    show_default=True,
    help="Video type: intro or main.",
)
@click.option(
    "--template-id",
    default=None,
    help="Template ID to use for generation.",
)
@click.option(
    "--product-url",
    default=None,
    help="URL of the product to feature in the video.",
)
@click.option(
    "--product-id",
    default=None,
    help="Product ID to use for generation.",
)
@click.option(
    "--user-images",
    default=None,
    help="JSON array of user image URLs.",
)
@click.option(
    "--user-videos",
    default=None,
    help="JSON array of user video URLs.",
)
@click.option(
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default="9:16",
    show_default=True,
    help="Aspect ratio of the output video.",
)
@click.option(
    "--language",
    type=click.Choice(LANGUAGES),
    default="zh",
    show_default=True,
    help="Language for the video content.",
)
@click.option(
    "--purpose",
    default=None,
    help="Purpose or goal of the video.",
)
@click.option(
    "--prompt",
    default=None,
    help="Text prompt to guide video generation.",
)
@click.option(
    "--nle-subtitle-enabled/--no-nle-subtitle-enabled",
    default=True,
    show_default=True,
    help="Enable NLE subtitle generation.",
)
@click.option(
    "--use-subtitle-erasure/--no-use-subtitle-erasure",
    default=False,
    show_default=True,
    help="Erase existing subtitles from source material.",
)
@click.option(
    "--watermark/--no-watermark",
    default=False,
    show_default=True,
    help="Add a watermark to the video.",
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
    duration: str,
    mode: str,
    video_type: str,
    template_id: str | None,
    product_url: str | None,
    product_id: str | None,
    user_images: str | None,
    user_videos: str | None,
    aspect_ratio: str,
    language: str,
    purpose: str | None,
    prompt: str | None,
    nle_subtitle_enabled: bool,
    use_subtitle_erasure: bool,
    watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate an e-commerce video.

    \\b
    Examples:
      kickart video --duration 15 --product-url https://example.com/product
      kickart video --duration 30 --mode pro --aspect-ratio 16:9 --language en
      kickart video --duration 15 --template-id tmpl_123 --async
    """
    client = get_client(ctx.obj.get("token"))

    parsed_user_images = _parse_json_array_option(user_images, "--user-images")
    parsed_user_videos = _parse_json_array_option(user_videos, "--user-videos")

    payload: dict[str, object] = {
        "duration": int(duration),
        "mode": mode,
        "type": video_type,
        "aspect_ratio": aspect_ratio,
        "language": language,
        "nle_subtitle_enabled": nle_subtitle_enabled,
        "use_subtitle_erasure": use_subtitle_erasure,
        "watermark": watermark,
    }
    if template_id is not None:
        payload["template_id"] = template_id
    if product_url is not None:
        payload["product_url"] = product_url
    if product_id is not None:
        payload["product_id"] = product_id
    if parsed_user_images is not None:
        payload["user_images"] = parsed_user_images
    if parsed_user_videos is not None:
        payload["user_videos"] = parsed_user_videos
    if purpose is not None:
        payload["purpose"] = purpose
    if prompt is not None:
        payload["prompt"] = prompt
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
    except KickartError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("viral-video")
@click.option(
    "--ref-video",
    required=True,
    help="URL of the reference video to base the viral video on.",
)
@click.option(
    "--language",
    type=click.Choice(LANGUAGES),
    required=True,
    help="Language for the video content.",
)
@click.option(
    "--mode",
    type=click.Choice(VIRAL_MODES),
    default="pro",
    show_default=True,
    help="Generation mode: pro or advanced.",
)
@click.option(
    "--template-id",
    default=None,
    help="Template ID to use.",
)
@click.option(
    "--product-url",
    default=None,
    help="URL of the product to feature.",
)
@click.option(
    "--product-id",
    default=None,
    help="Product ID to use.",
)
@click.option(
    "--product-images",
    default=None,
    help="JSON array of product image URLs.",
)
@click.option(
    "--model-images",
    default=None,
    help="JSON array of model image URLs.",
)
@click.option(
    "--ai-product-analysis/--no-ai-product-analysis",
    default=True,
    show_default=True,
    help="Enable AI-powered product analysis.",
)
@click.option(
    "--similarity",
    type=click.Choice(SIMILARITY_LEVELS),
    default="medium",
    show_default=True,
    help="Similarity level to the reference video (high or medium).",
)
@click.option(
    "--nle-subtitle-enabled/--no-nle-subtitle-enabled",
    default=True,
    show_default=True,
    help="Enable NLE subtitle generation.",
)
@click.option(
    "--use-subtitle-erasure/--no-use-subtitle-erasure",
    default=False,
    show_default=True,
    help="Erase existing subtitles from source material.",
)
@click.option(
    "--prompt",
    default=None,
    help="Text prompt to guide video generation.",
)
@click.option(
    "--location-images",
    default=None,
    help="JSON array of location image URLs.",
)
@click.option(
    "--watermark/--no-watermark",
    default=False,
    show_default=True,
    help="Add a watermark to the video.",
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
def viral_video(
    ctx: click.Context,
    ref_video: str,
    language: str,
    mode: str,
    template_id: str | None,
    product_url: str | None,
    product_id: str | None,
    product_images: str | None,
    model_images: str | None,
    ai_product_analysis: bool,
    similarity: str,
    nle_subtitle_enabled: bool,
    use_subtitle_erasure: bool,
    prompt: str | None,
    location_images: str | None,
    watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a viral e-commerce video from a reference video.

    \\b
    Examples:
      kickart viral-video --ref-video https://example.com/ref.mp4 --language en
      kickart viral-video --ref-video https://example.com/ref.mp4 --language zh --mode advanced
    """
    client = get_client(ctx.obj.get("token"))

    parsed_product_images = _parse_json_array_option(product_images, "--product-images")
    parsed_model_images = _parse_json_array_option(model_images, "--model-images")
    parsed_location_images = _parse_json_array_option(location_images, "--location-images")

    payload: dict[str, object] = {
        "ref_video": ref_video,
        "language": language,
        "mode": mode,
        "ai_product_analysis": ai_product_analysis,
        "similarity": similarity,
        "nle_subtitle_enabled": nle_subtitle_enabled,
        "use_subtitle_erasure": use_subtitle_erasure,
        "watermark": watermark,
    }
    if template_id is not None:
        payload["template_id"] = template_id
    if product_url is not None:
        payload["product_url"] = product_url
    if product_id is not None:
        payload["product_id"] = product_id
    if parsed_product_images is not None:
        payload["product_images"] = parsed_product_images
    if parsed_model_images is not None:
        payload["model_images"] = parsed_model_images
    if prompt is not None:
        payload["prompt"] = prompt
    if parsed_location_images is not None:
        payload["location_images"] = parsed_location_images
    if callback_url is not None:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate_viral_video(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KickartError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("template-video")
@click.option(
    "--template-id",
    required=True,
    help="Template ID to use for generation.",
)
@click.option(
    "--resource",
    "resource_list",
    required=True,
    help="JSON array of resource objects to use in the template.",
)
@click.option(
    "--resolution",
    default=None,
    help="Output resolution (e.g. 1080p).",
)
@click.option(
    "--watermark/--no-watermark",
    default=None,
    help="Add a watermark to the video.",
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
def template_video(
    ctx: click.Context,
    template_id: str,
    resource_list: str,
    resolution: str | None,
    watermark: bool | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from a Kickart template.

    RESOURCE is a JSON array of resource objects for the template.

    \\b
    Examples:
      kickart template-video --template-id tmpl_123 --resource '[{"type":"image","url":"https://example.com/img.jpg"}]'
      kickart template-video --template-id tmpl_123 --resource '[{"type":"video","url":"https://example.com/vid.mp4"}]' --async
    """
    client = get_client(ctx.obj.get("token"))

    parsed_resources = _parse_json_array_option(resource_list, "--resource")

    payload: dict[str, object] = {
        "template_id": template_id,
        "resource_list": parsed_resources,
    }
    if resolution is not None:
        payload["resolution"] = resolution
    if watermark is not None:
        payload["watermark"] = watermark
    if callback_url is not None:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate_template_video(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KickartError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Video generation commands."""

import click

from veo_cli.core.client import get_client
from veo_cli.core.exceptions import VeoError
from veo_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_MODEL,
    EXTEND_MODELS,
    MOTION_TYPES,
    RESOLUTIONS,
    UPSAMPLE_ACTIONS,
    VEO_MODELS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(VEO_MODELS),
    default=DEFAULT_MODEL,
    help="Veo model version.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution (4k, 1080p, gif).",
)
@click.option(
    "--translation/--no-translation",
    default=None,
    help="Enable automatic prompt translation.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    aspect_ratio: str,
    resolution: str | None,
    translation: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      veo generate "A cinematic scene of a sunset over the ocean"

      veo generate "A cat playing with yarn" -m veo3
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "text2video",
            "prompt": prompt,
            "model": model,
            "callback_url": callback_url,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "translation": translation,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    "image_urls",
    required=True,
    multiple=True,
    help="Image URL(s) for reference. Can be specified multiple times.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(VEO_MODELS),
    default=DEFAULT_MODEL,
    help="Veo model version.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution (4k, 1080p, gif).",
)
@click.option(
    "--translation/--no-translation",
    default=None,
    help="Enable automatic prompt translation.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    aspect_ratio: str,
    resolution: str | None,
    translation: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s).

    PROMPT describes the desired video. Provide one or more image URLs as reference.

    Examples:

      veo image-to-video "Animate this scene" -i https://example.com/photo.jpg

      veo image-to-video "Bring to life" -i img1.jpg -i img2.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            action="image2video",
            prompt=prompt,
            image_urls=list(image_urls),
            model=model,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            translation=translation,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("ingredients-to-video")
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    "image_urls",
    required=True,
    multiple=True,
    help="Ingredient image URL(s) (1-3). Can be specified multiple times.",
)
@click.option(
    "--translation/--no-translation",
    default=None,
    help="Enable automatic prompt translation.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def ingredients_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    translation: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from 1-3 ingredient images.

    PROMPT describes the desired video. Provide 1-3 ingredient image URLs.
    Uses the veo31-fast-ingredients model (forced by the API).

    Examples:

      veo ingredients-to-video "Product showcase" -i https://example.com/product.jpg

      veo ingredients-to-video "Scene" -i img1.jpg -i img2.jpg -i img3.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            action="ingredients2video",
            prompt=prompt,
            image_urls=list(image_urls),
            translation=translation,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("video_id")
@click.option(
    "-a",
    "--action",
    type=click.Choice(UPSAMPLE_ACTIONS),
    default="1080p",
    show_default=True,
    help="Upsample action: 1080p, 4k, or gif.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upscale(
    ctx: click.Context,
    video_id: str,
    action: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Upsample a generated video to a higher resolution.

    VIDEO_ID is the ID of the video to upsample.

    Examples:

      veo upscale abc123-def456

      veo upscale abc123-def456 --action 4k

      veo upscale abc123-def456 --action gif
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.upsample_video(
            action=action,
            video_id=video_id,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("video_id")
@click.option(
    "-m",
    "--model",
    type=click.Choice(EXTEND_MODELS),
    default="veo31-fast",
    show_default=True,
    help="Model for extending the video (veo31 series only).",
)
@click.option(
    "-p",
    "--prompt",
    default=None,
    help="Optional prompt guiding the extended section.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def extend(
    ctx: click.Context,
    video_id: str,
    model: str,
    prompt: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Extend a previously generated video.

    VIDEO_ID is the ID of the video to extend. Only veo31 series models are supported.

    Examples:

      veo extend abc123-def456

      veo extend abc123-def456 -m veo31 -p "slowly zoom out to reveal the landscape"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.extend_video(
            video_id=video_id,
            model=model,
            prompt=prompt,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("video_id")
@click.option(
    "--motion-type",
    type=click.Choice(MOTION_TYPES),
    required=True,
    help="Camera motion to apply when re-rendering the video.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def reshoot(
    ctx: click.Context,
    video_id: str,
    motion_type: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Re-render a video with a different camera motion.

    VIDEO_ID is the ID of the video to reshoot.

    Examples:

      veo reshoot abc123-def456 --motion-type LEFT_TO_RIGHT

      veo reshoot abc123-def456 --motion-type FORWARD
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.reshoot_video(
            video_id=video_id,
            motion_type=motion_type,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.group()
def objects() -> None:
    """Insert or remove objects in a video.

    \b
    Examples:
      veo objects insert abc123-def456 --prompt "add a flying pig with black wings"
      veo objects remove abc123-def456 --image-mask https://example.com/mask.jpg
    """


@objects.command()
@click.argument("video_id")
@click.option(
    "--prompt",
    required=True,
    help="Describes the object to add to the video.",
)
@click.option(
    "--image-mask",
    default=None,
    help="Optional mask image URL or base64 JPEG. White pixels indicate placement region.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def insert(
    ctx: click.Context,
    video_id: str,
    prompt: str,
    image_mask: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Insert an object into a video.

    VIDEO_ID is the ID of the video to edit.

    Examples:

      veo objects insert abc123-def456 --prompt "add a flying pig with black wings"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.edit_objects(
            action="insert",
            video_id=video_id,
            prompt=prompt,
            image_mask=image_mask,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@objects.command()
@click.argument("video_id")
@click.option(
    "--image-mask",
    required=True,
    help="Mask image (URL or base64 JPEG). White pixels define the region to remove.",
)
@click.option(
    "--prompt",
    default=None,
    help="Optional description of what to remove (for logging).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def remove(
    ctx: click.Context,
    video_id: str,
    image_mask: str,
    prompt: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Remove an object from a video using a mask.

    VIDEO_ID is the ID of the video to edit.

    Examples:

      veo objects remove abc123-def456 --image-mask https://example.com/mask.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.edit_objects(
            action="remove",
            video_id=video_id,
            image_mask=image_mask,
            prompt=prompt,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

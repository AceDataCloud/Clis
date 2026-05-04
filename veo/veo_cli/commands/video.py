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
    type=click.Choice(["1080p", "4k", "gif"]),
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
    """Upsample a generated video to higher resolution or GIF.

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
    required=True,
    help="Model to use for extending (veo31 or veo31-fast).",
)
@click.option("--prompt", default=None, help="Optional prompt guiding the extended section.")
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

    VIDEO_ID is the ID of the video to extend.

    Only Veo 3.1 series models are supported (veo31, veo31-fast).

    Examples:

      veo extend abc123-def456 -m veo31-fast

      veo extend abc123-def456 -m veo31 --prompt "Continue the scene"
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

    VIDEO_ID is the ID of the video to reshoot. Videos from `extend` cannot be used.

    Examples:

      veo reshoot abc123-def456 --motion-type FORWARD

      veo reshoot abc123-def456 --motion-type LEFT_TO_RIGHT
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


@click.command()
@click.argument("video_id")
@click.option(
    "-a",
    "--action",
    type=click.Choice(["insert", "remove"]),
    required=True,
    help="Object action: insert or remove.",
)
@click.option(
    "--prompt",
    default=None,
    help="Required for insert: describes what to add. Optional for remove.",
)
@click.option(
    "--image-mask",
    default=None,
    help=(
        "Mask image (URL or base64 JPEG). White pixels indicate the region to operate on. "
        "Required for remove; optional for insert."
    ),
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def objects(
    ctx: click.Context,
    video_id: str,
    action: str,
    prompt: str | None,
    image_mask: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Insert or remove objects in a generated video.

    VIDEO_ID is the ID of the video to edit. Videos from `extend` cannot be used.

    Examples:

      veo objects abc123 --action insert --prompt "Add a red balloon"

      veo objects abc123 --action remove --image-mask https://example.com/mask.jpg
    """
    if action == "insert" and not prompt:
        raise click.UsageError("--prompt is required when action is 'insert'.")
    if action == "remove" and not image_mask:
        raise click.UsageError("--image-mask is required when action is 'remove'.")

    client = get_client(ctx.obj.get("token"))
    try:
        result = client.edit_objects(
            video_id=video_id,
            action=action,
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

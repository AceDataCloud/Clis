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
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upscale(
    ctx: click.Context,
    video_id: str,
    output_json: bool,
) -> None:
    """Get 1080p version of a generated video.

    VIDEO_ID is the ID of the video to upscale.

    Examples:

      veo upscale abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.upscale_video(
            action="get1080p",
            video_id=video_id,
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
    help="What to produce: 1080p / 4k upscale, or animated gif preview.",
)
@click.option("--callback-url", help="Optional callback URL for async completion notification.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upsample(
    ctx: click.Context,
    video_id: str,
    action: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Upsample a generated video to 1080p / 4K, or render a GIF preview.

    VIDEO_ID is the id of the source video. Successor to `upscale` —
    use `upsample` whenever you want anything other than just 1080p.

    Examples:

      veo upsample abc123-def456 --action 4k
      veo upsample abc123-def456 --action gif
    """
    payload: dict = {"video_id": video_id, "action": action}
    if callback_url:
        payload["callback_url"] = callback_url
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.upsample_video(**payload)
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
    help="Model to extend with. Only the veo31 series is supported upstream.",
)
@click.option("-p", "--prompt", help="Optional prompt that guides the extended section.")
@click.option("--callback-url", help="Optional callback URL for async completion notification.")
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
    """Extend the duration of a previously generated video.

    Adds extra seconds to the end of an existing video. The model
    continues the scene; an optional --prompt steers what happens next.

    Outputs of `extend` can be extended further but cannot be reshot
    or object-edited (upstream limitation, returns 400 if attempted).

    Examples:

      veo extend abc123-def456
      veo extend abc123-def456 -m veo31 -p "the camera zooms out"
    """
    payload: dict = {"video_id": video_id, "model": model}
    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.extend_video(**payload)
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
    "-t",
    "--motion-type",
    type=click.Choice(MOTION_TYPES, case_sensitive=False),
    required=True,
    help="Camera motion to apply (e.g. LEFT_TO_RIGHT, FORWARD, DOLLY_IN_ZOOM_OUT).",
)
@click.option("--callback-url", help="Optional callback URL for async completion notification.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def reshoot(
    ctx: click.Context,
    video_id: str,
    motion_type: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Re-render an existing video with a different camera motion.

    Keeps the same scene content but changes how the camera moves
    through it. Useful for trying alternative shot framings cheaply.

    Not supported on outputs of `extend`.

    Available motion types:
      STATIONARY, STATIONARY_UP, STATIONARY_DOWN, STATIONARY_LEFT,
      STATIONARY_RIGHT, STATIONARY_DOLLY_IN_ZOOM_OUT,
      STATIONARY_DOLLY_OUT_ZOOM_IN, UP, DOWN, LEFT_TO_RIGHT,
      RIGHT_TO_LEFT, FORWARD, BACKWARD, DOLLY_IN_ZOOM_OUT,
      DOLLY_OUT_ZOOM_IN.

    Examples:

      veo reshoot abc123-def456 --motion-type LEFT_TO_RIGHT
      veo reshoot abc123-def456 -t DOLLY_IN_ZOOM_OUT
    """
    payload: dict = {"video_id": video_id, "motion_type": motion_type.upper()}
    if callback_url:
        payload["callback_url"] = callback_url
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.reshoot_video(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("object-insert")
@click.argument("video_id")
@click.argument("prompt")
@click.option(
    "--mask",
    "image_mask",
    help="Optional mask: HTTP(S) URL or base64-encoded JPEG. White pixels mark insertion zone. If omitted, AI auto-determines placement.",
)
@click.option("--callback-url", help="Optional callback URL for async completion notification.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def object_insert(
    ctx: click.Context,
    video_id: str,
    prompt: str,
    image_mask: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Insert an object into a previously generated video.

    Adds a new element to an existing scene. Provide a PROMPT describing
    what to add. Optionally provide --mask to control placement.

    Not supported on outputs of `extend`.

    Examples:

      veo object-insert abc123 "add a flying pig with black wings"
      veo object-insert abc123 "add fireworks" --mask https://example.com/mask.jpg
    """
    payload: dict = {"video_id": video_id, "action": "insert", "prompt": prompt}
    if image_mask:
        payload["image_mask"] = image_mask
    if callback_url:
        payload["callback_url"] = callback_url
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.manipulate_object(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("object-remove")
@click.argument("video_id")
@click.argument("image_mask")
@click.option("-p", "--prompt", help="Optional description of what is being removed (logs only).")
@click.option("--callback-url", help="Optional callback URL for async completion notification.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def object_remove(
    ctx: click.Context,
    video_id: str,
    image_mask: str,
    prompt: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Remove an object from a previously generated video.

    IMAGE_MASK is required: HTTP(S) URL or base64-encoded JPEG. White
    pixels mark the region to erase; the AI inpaints the gap with
    contextually appropriate content.

    Not supported on outputs of `extend`.

    Examples:

      veo object-remove abc123 https://example.com/mask.jpg
      veo object-remove abc123 https://example.com/mask.jpg -p "remove the cloud"
    """
    payload: dict = {"video_id": video_id, "action": "remove", "image_mask": image_mask}
    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.manipulate_object(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

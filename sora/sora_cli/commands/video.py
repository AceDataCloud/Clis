"""Video generation commands."""

import click

from sora_cli.core.client import get_client
from sora_cli.core.exceptions import SoraError
from sora_cli.core.output import (
    DEFAULT_MODEL,
    DEFAULT_SIZE,
    SORA_DURATIONS,
    SORA_MODELS,
    SORA_SIZES,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SORA_MODELS),
    default=DEFAULT_MODEL,
    help="Sora model version.",
)
@click.option(
    "--orientation",
    type=click.Choice(["landscape", "portrait"]),
    default="landscape",
    help="Video orientation. Only applicable for version 1.0.",
)
@click.option(
    "--duration",
    type=click.Choice(SORA_DURATIONS),
    default="15",
    help="Duration in seconds. For v1.0: 10 or 15 (sora-2), or 10, 15, 25 (sora-2-pro). For v2.0: 4, 8, or 12.",
)
@click.option(
    "--size",
    type=click.Choice(SORA_SIZES),
    default=DEFAULT_SIZE,
    help="Video size/resolution. For v1.0: small or large. For v2.0: pixel resolution (e.g. 720x1280).",
)
@click.option(
    "--version",
    type=click.Choice(["1.0", "2.0"]),
    default="1.0",
    help="API version. 1.0 supports orientation/character params; 2.0 supports pixel-based sizes.",
)
@click.option(
    "--character-url", default=None, help="Video URL of the character to use (v1.0 only)."
)
@click.option(
    "--character-start",
    type=int,
    default=None,
    help="Starting second for the character appearance (v1.0, required when --character-url is set).",
)
@click.option(
    "--character-end",
    type=int,
    default=None,
    help="Ending second for the character appearance (v1.0, required when --character-url is set).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    orientation: str,
    duration: str,
    size: str,
    version: str,
    character_url: str | None,
    character_start: int | None,
    character_end: int | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      sora generate "A cinematic scene of a sunset over the ocean"

      sora generate "A cat playing with yarn" -m sora-2

      sora generate "A hero scene" --version 2.0 --size 1280x720 --duration 8
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "callback_url": callback_url,
            "orientation": orientation,
            "duration": int(duration),
            "size": size,
            "version": version,
            "character_url": character_url,
            "character_start": character_start,
            "character_end": character_end,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except SoraError as e:
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
    type=click.Choice(SORA_MODELS),
    default=DEFAULT_MODEL,
    help="Sora model version.",
)
@click.option(
    "--orientation",
    type=click.Choice(["landscape", "portrait"]),
    default="landscape",
    help="Video orientation. Only applicable for version 1.0.",
)
@click.option(
    "--duration",
    type=click.Choice(SORA_DURATIONS),
    default="15",
    help="Duration in seconds. For v1.0: 10 or 15 (sora-2), or 10, 15, 25 (sora-2-pro). For v2.0: 4, 8, or 12.",
)
@click.option(
    "--size",
    type=click.Choice(SORA_SIZES),
    default=DEFAULT_SIZE,
    help="Video size/resolution. For v1.0: small or large. For v2.0: pixel resolution (e.g. 720x1280).",
)
@click.option(
    "--version",
    type=click.Choice(["1.0", "2.0"]),
    default="1.0",
    help="API version. 1.0 supports orientation/multiple images; 2.0 uses first image and pixel-based sizes.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    orientation: str,
    duration: str,
    size: str,
    version: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s).

    PROMPT describes the desired video. Provide one or more image URLs as reference.

    Examples:

      sora image-to-video "Animate this scene" -i https://example.com/photo.jpg

      sora image-to-video "Bring to life" -i img1.jpg -i img2.jpg

      sora image-to-video "Action shot" -i img.jpg --version 2.0 --size 1280x720
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            prompt=prompt,
            image_urls=list(image_urls),
            model=model,
            orientation=orientation,
            duration=int(duration),
            size=size,
            version=version,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except SoraError as e:
        print_error(e.message)
        raise SystemExit(1) from e

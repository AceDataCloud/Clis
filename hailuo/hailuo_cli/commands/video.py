"""Video generation commands."""

import click

from hailuo_cli.core.client import get_client
from hailuo_cli.core.exceptions import HailuoError
from hailuo_cli.core.output import (
    DEFAULT_MODEL,
    HAILUO_MODELS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(HAILUO_MODELS),
    default=DEFAULT_MODEL,
    help="Hailuo model to use (default: minimax-t2v).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    \b
    Examples:
      hailuo generate "A cat playing in the snow"
      hailuo generate "Ocean waves at sunset" --model minimax-t2v
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "model": model,
            "callback_url": callback_url,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HailuoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option(
    "--image-url", required=True, help="URL of the first frame reference image."
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(["minimax-i2v", "minimax-i2v-director"]),
    default="minimax-i2v",
    help="Hailuo image-to-video model (default: minimax-i2v).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_url: str,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from an image and text prompt.

    PROMPT describes the desired video content.

    \b
    Examples:
      hailuo image-to-video "Animate this scene" --image-url https://example.com/photo.jpg
      hailuo image-to-video "Cinematic pan" --image-url img.jpg --model minimax-i2v-director
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "model": model,
            "first_image_url": image_url,
            "callback_url": callback_url,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except HailuoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Video generation commands."""

import click

from gemini_cli.core.client import get_client
from gemini_cli.core.exceptions import GeminiError
from gemini_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_VIDEO_MODEL,
    GEMINI_VIDEO_MODELS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(GEMINI_VIDEO_MODELS),
    default=DEFAULT_VIDEO_MODEL,
    show_default=True,
    help="Gemini video model to use.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    show_default=True,
    help="Aspect ratio of the output video.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    aspect_ratio: str,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    \b
    Examples:
      gemini generate "A cinematic scene of a sunset over the ocean"
      gemini generate "A cat playing with yarn" --aspect-ratio 9:16
      gemini generate "Dancing robots" --async
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "callback_url": callback_url,
            **({"async": True} if async_mode else {}),
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except GeminiError as e:
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
    type=click.Choice(GEMINI_VIDEO_MODELS),
    default=DEFAULT_VIDEO_MODEL,
    show_default=True,
    help="Gemini video model to use.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    show_default=True,
    help="Aspect ratio of the output video.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    aspect_ratio: str,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s).

    PROMPT describes the desired video. Provide one or more image URLs as reference.

    \b
    Examples:
      gemini image-to-video "Animate this scene" -i https://example.com/photo.jpg
      gemini image-to-video "Bring to life" -i img1.jpg -i img2.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            prompt=prompt,
            image_urls=list(image_urls),
            model=model,
            aspect_ratio=aspect_ratio,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except GeminiError as e:
        print_error(e.message)
        raise SystemExit(1) from e

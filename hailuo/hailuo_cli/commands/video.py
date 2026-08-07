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

RESOLUTION_CHOICES = ["768P", "2K"]
RATIO_CHOICES = ["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
CONTENT_ROLE_CHOICES = [
    "first_frame",
    "last_frame",
    "reference_image",
    "reference_video",
    "reference_audio",
]


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "-m",
    "--model",
    type=click.Choice(HAILUO_MODELS),
    default=DEFAULT_MODEL,
    help="Hailuo model to use (default: MiniMax-H3).",
)
@click.option(
    "--image-url",
    "image_urls",
    multiple=True,
    help="Image URL input (repeat as needed).",
)
@click.option(
    "--image-role",
    type=click.Choice(CONTENT_ROLE_CHOICES),
    multiple=True,
    help="Role for each --image-url, in the same order.",
)
@click.option(
    "--video-url",
    "video_urls",
    multiple=True,
    help="Video URL input (repeat as needed).",
)
@click.option(
    "--video-role",
    type=click.Choice(CONTENT_ROLE_CHOICES),
    multiple=True,
    help="Role for each --video-url, in the same order.",
)
@click.option(
    "--audio-url",
    "audio_urls",
    multiple=True,
    help="Audio URL input (repeat as needed).",
)
@click.option(
    "--audio-role",
    type=click.Choice(CONTENT_ROLE_CHOICES),
    multiple=True,
    help="Role for each --audio-url, in the same order.",
)
@click.option(
    "--ratio",
    type=click.Choice(RATIO_CHOICES),
    default="adaptive",
    show_default=True,
    help="Output aspect ratio.",
)
@click.option(
    "--duration",
    type=click.IntRange(4, 15),
    default=4,
    show_default=True,
    help="Output duration in seconds.",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="2K",
    show_default=True,
    help="Output resolution.",
)
@click.option(
    "--aigc-watermark/--no-aigc-watermark",
    default=False,
    show_default=True,
    help="Whether to enable AIGC watermark.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str | None,
    model: str,
    image_urls: tuple[str, ...],
    image_role: tuple[str, ...],
    video_urls: tuple[str, ...],
    video_role: tuple[str, ...],
    audio_urls: tuple[str, ...],
    audio_role: tuple[str, ...],
    ratio: str,
    duration: int,
    resolution: str,
    aigc_watermark: bool,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    \b
    Examples:
      hailuo generate "A cat playing in the snow"
      hailuo generate "Ocean waves at sunset" --model MiniMax-H3
    """
    client = get_client(ctx.obj.get("token"))
    try:
        if not prompt and not image_urls and not video_urls and not audio_urls:
            raise click.UsageError(
                "Provide PROMPT or at least one media URL input."
            )
        if prompt and len(prompt) > 7000:
            raise click.UsageError("PROMPT must be at most 7000 characters.")
        content: list[dict[str, object]] = []
        if prompt:
            content.append({"type": "text", "text": prompt})
        for content_type, urls, roles in (
            ("image_url", image_urls, image_role),
            ("video_url", video_urls, video_role),
            ("audio_url", audio_urls, audio_role),
        ):
            if roles and len(urls) != len(roles):
                raise click.UsageError(
                    f"Provide one --{content_type.removesuffix('_url')}-role for each "
                    f"--{content_type.replace('_', '-')}."
                )
            for index, url in enumerate(urls):
                item: dict[str, object] = {"type": content_type, content_type: {"url": url}}
                if roles:
                    item["role"] = roles[index]
                content.append(item)

        payload: dict[str, object] = {
            "model": model,
            "content": content,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "aigc_watermark": aigc_watermark,
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
@click.option("--image-url", required=True, help="URL of the first frame reference image.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(HAILUO_MODELS),
    default=DEFAULT_MODEL,
    help="Hailuo image-to-video model (default: MiniMax-H3).",
)
@click.option(
    "--ratio",
    type=click.Choice(RATIO_CHOICES),
    default="adaptive",
    show_default=True,
    help="Output aspect ratio.",
)
@click.option(
    "--duration",
    type=click.IntRange(4, 15),
    default=4,
    show_default=True,
    help="Output duration in seconds.",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTION_CHOICES),
    default="2K",
    show_default=True,
    help="Output resolution.",
)
@click.option(
    "--aigc-watermark/--no-aigc-watermark",
    default=False,
    show_default=True,
    help="Whether to enable AIGC watermark.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_url: str,
    model: str,
    ratio: str,
    duration: int,
    resolution: str,
    aigc_watermark: bool,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from an image and text prompt.

    PROMPT describes the desired video content.

    \b
    Examples:
      hailuo image-to-video "Animate this scene" --image-url https://example.com/photo.jpg
      hailuo image-to-video "Cinematic pan" --image-url img.jpg --model MiniMax-H3
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "model": model,
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                    "role": "first_frame",
                },
            ],
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "aigc_watermark": aigc_watermark,
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

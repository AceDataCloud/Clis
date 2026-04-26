"""Image generation and editing commands."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_GENERATION_MODEL,
    DEFAULT_IMAGE_MODEL,
    GENERATION_MODELS,
    IMAGE_MODELS,
    print_error,
    print_image_result,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(GENERATION_MODELS),
    default=DEFAULT_GENERATION_MODEL,
    show_default=True,
    help="Image generation model to use.",
)
@click.option(
    "-n",
    "--count",
    default=None,
    type=int,
    help="Number of images to generate (1-10).",
)
@click.option(
    "-s",
    "--size",
    type=click.Choice(["1024x1024", "1792x1024", "1024x1792", "1536x1024", "1024x1536", "256x256", "512x512", "auto"]),
    default=None,
    help="Size of the generated image.",
)
@click.option(
    "--quality",
    type=click.Choice(["auto", "high", "medium", "low", "hd", "standard"]),
    default=None,
    help="Image quality.",
)
@click.option(
    "--style",
    type=click.Choice(["vivid", "natural"]),
    default=None,
    help="Style for dall-e-3: vivid or natural.",
)
@click.option(
    "--output-format",
    type=click.Choice(["png", "jpeg", "webp"]),
    default=None,
    help="Output format for GPT image models.",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque", "auto"]),
    default=None,
    help="Background transparency for GPT image models.",
)
@click.option(
    "--moderation",
    type=click.Choice(["low", "auto"]),
    default=None,
    help="Content-moderation level for GPT image models.",
)
@click.option(
    "--output-compression",
    default=None,
    type=click.IntRange(0, 100),
    help="Compression level (0-100) for webp/jpeg output.",
)
@click.option(
    "--partial-images",
    default=None,
    type=click.IntRange(0, 3),
    help="Number of partial images to emit during streaming (0-3).",
)
@click.option(
    "--response-format",
    type=click.Choice(["url", "b64_json"]),
    default=None,
    help="Format for dall-e image responses.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async image generation.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image(
    ctx: click.Context,
    prompt: str,
    model: str,
    count: int | None,
    size: str | None,
    quality: str | None,
    style: str | None,
    output_format: str | None,
    background: str | None,
    moderation: str | None,
    output_compression: int | None,
    partial_images: int | None,
    response_format: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate an image from a text prompt.

    PROMPT is the text description of the desired image.

    \b
    Examples:
      openai-cli image "A futuristic city skyline at night"
      openai-cli image "Portrait of a cat" -m gpt-image-1 --quality high
      openai-cli image "Abstract art" --size 1792x1024 --style vivid
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "prompt": prompt,
        "model": model,
        "n": count,
        "size": size,
        "quality": quality,
        "style": style,
        "output_format": output_format,
        "background": background,
        "moderation": moderation,
        "output_compression": output_compression,
        "partial_images": partial_images,
        "response_format": response_format,
        "callback_url": callback_url,
    }

    try:
        result = client.image_generations(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt")
@click.option(
    "--image-url",
    required=True,
    help="URL of the reference image to edit.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(IMAGE_MODELS),
    default=DEFAULT_IMAGE_MODEL,
    show_default=True,
    help="Image editing model to use.",
)
@click.option(
    "-n",
    "--count",
    default=None,
    type=int,
    help="Number of images to generate (1-10).",
)
@click.option(
    "-s",
    "--size",
    type=click.Choice(["1024x1024", "1536x1024", "1024x1536", "256x256", "512x512", "auto"]),
    default=None,
    help="Size of the output image.",
)
@click.option(
    "--quality",
    type=click.Choice(["auto", "high", "medium", "low", "standard"]),
    default=None,
    help="Image quality.",
)
@click.option(
    "--output-format",
    type=click.Choice(["png", "jpeg", "webp"]),
    default=None,
    help="Output format for GPT image models.",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque", "auto"]),
    default=None,
    help="Background transparency for GPT image models.",
)
@click.option(
    "--input-fidelity",
    type=click.Choice(["high", "low"]),
    default=None,
    help="How strongly to match input style/features (GPT image models only).",
)
@click.option(
    "--output-compression",
    default=None,
    type=click.IntRange(0, 100),
    help="Compression level (0-100) for webp/jpeg output.",
)
@click.option(
    "--response-format",
    type=click.Choice(["url", "b64_json"]),
    default=None,
    help="Response format: url or b64_json.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async image editing.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edit(
    ctx: click.Context,
    prompt: str,
    image_url: str,
    model: str,
    count: int | None,
    size: str | None,
    quality: str | None,
    output_format: str | None,
    background: str | None,
    input_fidelity: str | None,
    output_compression: int | None,
    response_format: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Edit an image using a text prompt.

    PROMPT describes the changes to make to the reference image.

    \b
    Examples:
      openai-cli edit "Add a rainbow" --image-url https://example.com/photo.jpg
      openai-cli edit "Change background to forest" --image-url https://example.com/pic.jpg -m gpt-image-1
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "prompt": prompt,
        "image": image_url,
        "model": model,
        "n": count,
        "size": size,
        "quality": quality,
        "output_format": output_format,
        "background": background,
        "input_fidelity": input_fidelity,
        "output_compression": output_compression,
        "response_format": response_format,
        "callback_url": callback_url,
    }

    try:
        result = client.image_edits(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

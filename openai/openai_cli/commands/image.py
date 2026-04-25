"""Image generation and editing commands."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_IMAGE_MODEL,
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
    type=click.Choice(IMAGE_MODELS),
    default=DEFAULT_IMAGE_MODEL,
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

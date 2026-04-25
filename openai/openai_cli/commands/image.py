"""Image generation and editing commands."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_IMAGE_MODEL,
    IMAGE_MODELS,
    IMAGE_OUTPUT_FORMATS,
    IMAGE_QUALITY,
    IMAGE_SIZES,
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
    help="Image generation model.",
)
@click.option(
    "-n",
    "--number",
    type=int,
    default=None,
    help="Number of images to generate (1-10).",
)
@click.option(
    "--size",
    type=click.Choice(IMAGE_SIZES),
    default=None,
    help="Size of the generated image.",
)
@click.option(
    "--quality",
    type=click.Choice(IMAGE_QUALITY),
    default=None,
    help="Quality of the generated image.",
)
@click.option(
    "--output-format",
    type=click.Choice(IMAGE_OUTPUT_FORMATS),
    default=None,
    help="Output format for GPT image models (png, jpeg, webp).",
)
@click.option(
    "--style",
    type=click.Choice(["vivid", "natural"]),
    default=None,
    help="Style for dall-e-3: vivid (hyper-real) or natural (more neutral).",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque", "auto"]),
    default=None,
    help="Transparency setting for GPT image models.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def imagine(
    ctx: click.Context,
    prompt: str,
    model: str,
    number: int | None,
    size: str | None,
    quality: str | None,
    output_format: str | None,
    style: str | None,
    background: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate an image from a text prompt.

    PROMPT is a detailed description of the image to generate.

    \b
    Examples:
      openai imagine "A cat sitting on a windowsill at sunset"
      openai imagine "Product photo of a watch" -m gpt-image-1 --quality high
      openai imagine "Abstract landscape" --size 1536x1024 --style vivid
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "n": number,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "style": style,
            "background": background,
            "callback_url": callback_url,
        }

        result = client.generate_image(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("edit-image")
@click.argument("prompt")
@click.option(
    "-i",
    "--image",
    "image_urls",
    required=True,
    multiple=True,
    help="Reference image URL(s). Can be specified multiple times.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(IMAGE_MODELS),
    default=DEFAULT_IMAGE_MODEL,
    help="Image editing model.",
)
@click.option(
    "-n",
    "--number",
    type=int,
    default=None,
    help="Number of images to generate (1-10).",
)
@click.option(
    "--size",
    type=click.Choice(IMAGE_SIZES),
    default=None,
    help="Size of the output image.",
)
@click.option(
    "--quality",
    type=click.Choice(IMAGE_QUALITY),
    default=None,
    help="Quality of the output image.",
)
@click.option(
    "--output-format",
    type=click.Choice(IMAGE_OUTPUT_FORMATS),
    default=None,
    help="Output format (png, jpeg, webp).",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque", "auto"]),
    default=None,
    help="Transparency handling for GPT image models.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edit_image(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    number: int | None,
    size: str | None,
    quality: str | None,
    output_format: str | None,
    background: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Edit an image using a text prompt.

    PROMPT is a description of the desired edit.

    \b
    Examples:
      openai edit-image "Make the background white" -i https://example.com/photo.jpg
      openai edit-image "Add sunglasses" -i photo1.jpg -m gpt-image-1
    """
    client = get_client(ctx.obj.get("token"))
    try:
        image: object = list(image_urls) if len(image_urls) > 1 else image_urls[0]

        payload: dict[str, object] = {
            "prompt": prompt,
            "image": image,
            "model": model,
            "n": number,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "background": background,
            "callback_url": callback_url,
        }

        result = client.edit_image(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

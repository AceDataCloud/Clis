"""Image generation and editing commands."""

import click

from nanobanana_cli.core.client import get_client
from nanobanana_cli.core.exceptions import NanoBananaError
from nanobanana_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_MODEL,
    NANOBANANA_MODELS,
    RESOLUTIONS,
    print_error,
    print_image_result,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(NANOBANANA_MODELS),
    default=DEFAULT_MODEL,
    help="NanoBanana model version.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of generated image.",
)
@click.option(
    "-r",
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution (nano-banana-pro only).",
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
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate an image from a text prompt.

    PROMPT is a detailed description of the image to generate. Include subject,
    atmosphere, lighting, camera/lens, and quality keywords for best results.

    Examples:

      nanobanana generate "A cat sitting on a windowsill at sunset"

      nanobanana generate "Product photo of a watch" -m nano-banana-pro -r 4K

      nanobanana generate "Landscape painting" -a 16:9
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "callback_url": callback_url,
        }
        if resolution:
            payload["resolution"] = resolution

        result = client.generate_image(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except NanoBananaError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    "image_urls",
    required=True,
    multiple=True,
    help="Image URL(s) to edit. Can be specified multiple times.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(NANOBANANA_MODELS),
    default=DEFAULT_MODEL,
    help="NanoBanana model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edit(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Edit or combine images using AI.

    PROMPT describes the desired edit. Use with one or more image URLs.

    Use cases: virtual try-on, product placement, style transfer, image restoration,
    2D to 3D conversion, poster editing.

    Examples:

      nanobanana edit "Let this person wear this T-shirt" -i person.jpg -i shirt.jpg

      nanobanana edit "Place this product in a modern kitchen" -i product.jpg

      nanobanana edit "Convert to oil painting style" -i photo.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.edit_image(
            action="edit",
            prompt=prompt,
            image_urls=list(image_urls),
            model=model,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except NanoBananaError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Image generation and editing commands."""

import click

from qwen_image_cli.core.client import get_client
from qwen_image_cli.core.exceptions import QwenImageError
from qwen_image_cli.core.output import (
    DEFAULT_MODEL,
    PROMPT_EXTEND_MODES,
    QWEN_IMAGE_MODELS,
    print_error,
    print_image_result,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(QWEN_IMAGE_MODELS),
    default=DEFAULT_MODEL,
    help="Qwen Image model version.",
)
@click.option(
    "-n",
    "--n",
    type=click.IntRange(1, 6),
    default=1,
    help="Number of images to generate (1-6, default 1).",
)
@click.option(
    "--size",
    default=None,
    help="Output image size (for example: 1024*1024).",
)
@click.option(
    "--prompt-extend/--no-prompt-extend",
    default=True,
    help="Enable or disable prompt extension (default: enabled).",
)
@click.option(
    "--prompt-extend-mode",
    type=click.Choice(PROMPT_EXTEND_MODES),
    default="direct",
    help="Prompt extension mode.",
)
@click.option(
    "--enable-thinking/--no-enable-thinking",
    default=True,
    help="Enable or disable model thinking mode (default: enabled).",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Elements to avoid in the generated image.",
)
@click.option(
    "--seed",
    type=click.IntRange(0, 2147483647),
    default=None,
    help="Random seed for reproducible generation.",
)
@click.option(
    "--watermark/--no-watermark",
    default=False,
    help="Enable or disable output watermark (default: disabled).",
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
    n: int,
    size: str | None,
    prompt_extend: bool,
    prompt_extend_mode: str,
    enable_thinking: bool,
    negative_prompt: str | None,
    seed: int | None,
    watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate an image from a text prompt.

    PROMPT is a detailed description of the image to generate. Include subject,
    atmosphere, lighting, camera/lens, and quality keywords for best results.

    Examples:

      qwen-image generate "A cat sitting on a windowsill at sunset"

      qwen-image generate "Product photo of a watch" -m qwen-image-3.0-pro --size 1024*1536
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "n": n,
            "size": size,
            "prompt_extend": prompt_extend,
            "prompt_extend_mode": prompt_extend_mode,
            "enable_thinking": enable_thinking,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "watermark": watermark,
            "callback_url": callback_url,
            "async": async_mode,
        }

        result = client.generate_image(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except QwenImageError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    "image_urls",
    multiple=True,
    required=True,
    help="Image URL(s) to edit. Can be specified multiple times.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(QWEN_IMAGE_MODELS),
    default=DEFAULT_MODEL,
    help="Qwen Image model version.",
)
@click.option(
    "-n",
    "--n",
    type=click.IntRange(1, 6),
    default=1,
    help="Number of images to generate (1-6, default 1).",
)
@click.option(
    "--size",
    default=None,
    help="Output image size (for example: 1024*1024).",
)
@click.option(
    "--prompt-extend/--no-prompt-extend",
    default=True,
    help="Enable or disable prompt extension (default: enabled).",
)
@click.option(
    "--prompt-extend-mode",
    type=click.Choice(PROMPT_EXTEND_MODES),
    default="direct",
    help="Prompt extension mode.",
)
@click.option(
    "--enable-thinking/--no-enable-thinking",
    default=True,
    help="Enable or disable model thinking mode (default: enabled).",
)
@click.option(
    "--negative-prompt",
    default=None,
    help="Elements to avoid in the generated image.",
)
@click.option(
    "--seed",
    type=click.IntRange(0, 2147483647),
    default=None,
    help="Random seed for reproducible generation.",
)
@click.option(
    "--watermark/--no-watermark",
    default=False,
    help="Enable or disable output watermark (default: disabled).",
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
def edit(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    n: int,
    size: str | None,
    prompt_extend: bool,
    prompt_extend_mode: str,
    enable_thinking: bool,
    negative_prompt: str | None,
    seed: int | None,
    watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Edit or combine images using AI.

    PROMPT describes the desired edit. Use with one or more image URLs.

    Use cases: virtual try-on, product placement, style transfer, image restoration,
    2D to 3D conversion, poster editing.

    Examples:

      qwen-image edit "Let this person wear this T-shirt" -i person.jpg -i shirt.jpg

      qwen-image edit "Place this product in a modern kitchen" -i product.jpg

      qwen-image edit "Convert to oil painting style" -i photo.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        if len(image_urls) > 3:
            print_error("A maximum of 3 image URLs can be provided.")
            raise SystemExit(1)

        payload: dict[str, object] = {
            "prompt": prompt,
            "image_urls": list(image_urls),
            "model": model,
            "n": n,
            "size": size,
            "prompt_extend": prompt_extend,
            "prompt_extend_mode": prompt_extend_mode,
            "enable_thinking": enable_thinking,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "watermark": watermark,
            "callback_url": callback_url,
            "async": async_mode,
        }
        result = client.edit_image(
            **payload,  # type: ignore[arg-type]
        )
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except QwenImageError as e:
        print_error(e.message)
        raise SystemExit(1) from e

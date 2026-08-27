"""Image generation and editing commands."""

import re
from pathlib import Path

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

_SIZE_PATTERN = re.compile(r"^(auto|\d+x\d+)$")


def _validate_size_format(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> str | None:
    """Validate that size matches 'auto' or 'WIDTHxHEIGHT' pattern."""
    if value is not None and not _SIZE_PATTERN.match(value):
        raise click.BadParameter(
            f"'{value}' is not a valid size. Use 'auto' or 'WIDTHxHEIGHT' format (e.g. 1024x1024).",
            ctx=ctx,
            param=param,
        )
    return value


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
    type=click.IntRange(1, 10),
    help="Number of images to generate (1-10).",
)
@click.option(
    "-s",
    "--size",
    default=None,
    callback=_validate_size_format,
    is_eager=False,
    help=(
        "Size of the generated image as WIDTHxHEIGHT or 'auto'. "
        "gpt-image-2 accepts any WIDTHxHEIGHT (multiples of 16, max 3840 on each side). "
        "dall-e-3: 1024x1024, 1792x1024, 1024x1792. "
        "dall-e-2: 256x256, 512x512, 1024x1024."
    ),
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
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
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
    async_mode: bool,
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
        "async": async_mode,
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
    multiple=True,
    help="Reference image URL to edit (repeat up to 16 times).",
)
@click.option(
    "--image-file",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Reference image file to upload for editing (repeat up to 16 times).",
)
@click.option(
    "--mask-file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Optional mask image file for uploaded image edits.",
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
    type=click.IntRange(1, 10),
    help="Number of images to generate (1-10).",
)
@click.option(
    "-s",
    "--size",
    default=None,
    callback=_validate_size_format,
    is_eager=False,
    help=(
        "Size of the output image as WIDTHxHEIGHT or 'auto'. "
        "gpt-image-2 accepts any WIDTHxHEIGHT (multiples of 16, max 3840 on each side). "
        "dall-e-3: 1024x1024, 1792x1024, 1024x1792. "
        "dall-e-2: 256x256, 512x512, 1024x1024."
    ),
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
    "--partial-images",
    default=None,
    type=click.IntRange(0, 3),
    help="Number of partial images to emit during streaming (0-3).",
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
    image_url: tuple[str, ...],
    image_file: tuple[str, ...],
    mask_file: str | None,
    model: str,
    count: int | None,
    size: str | None,
    quality: str | None,
    output_format: str | None,
    background: str | None,
    input_fidelity: str | None,
    output_compression: int | None,
    partial_images: int | None,
    response_format: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Edit an image using a text prompt.

    PROMPT describes the changes to make to the reference image.

    \b
    Examples:
      openai-cli edit "Add a rainbow" --image-url https://example.com/photo.jpg
      openai-cli edit "Change background to forest" --image-url https://example.com/pic.jpg -m gpt-image-1
      openai-cli edit "Remove background" --image-file photo.png --mask-file mask.png
    """
    if not image_url and not image_file:
        raise click.UsageError("Provide at least one of --image-url or --image-file.")
    if image_url and image_file:
        raise click.UsageError("Use either --image-url or --image-file, not both.")
    if image_url and (mask_file or partial_images is not None):
        raise click.UsageError("--mask-file and --partial-images require --image-file.")
    if len(image_url) > 16:
        raise click.UsageError("Provide at most 16 --image-url options.")
    if len(image_file) > 16:
        raise click.UsageError("Provide at most 16 --image-file options.")

    client = get_client(ctx.obj.get("token"))
    if image_file:
        if model == "nano-banana-2-lite":
            raise click.UsageError(
                "--model nano-banana-2-lite is not supported with --image-file uploads. "
                "Use --image-url or choose a different model."
            )
        fields: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "n": count,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "background": background,
            "input_fidelity": input_fidelity,
            "output_compression": output_compression,
            "partial_images": partial_images,
            "response_format": response_format,
            "callback_url": callback_url,
            "async": async_mode,
        }
        files: list[tuple[str, object]] = [
            ("image", (Path(path).name, Path(path).read_bytes(), "application/octet-stream"))
            for path in image_file
        ]
        if mask_file:
            mask_path = Path(mask_file)
            files.append(
                ("mask", (mask_path.name, mask_path.read_bytes(), "application/octet-stream"))
            )

        try:
            result = client.image_edits_multipart(fields=fields, files=files)
            if output_json:
                print_json(result)
            else:
                print_image_result(result)
            return
        except OpenAIError as e:
            print_error(e.message)
            raise SystemExit(1) from e

    image: str | list[str] = image_url[0] if len(image_url) == 1 else list(image_url)
    payload: dict[str, object] = {
        "prompt": prompt,
        "image": image,
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
        "async": async_mode,
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

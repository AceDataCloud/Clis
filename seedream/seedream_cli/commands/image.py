"""Image generation commands."""

import re

import click

from seedream_cli.core.client import get_client
from seedream_cli.core.exceptions import SeedreamError
from seedream_cli.core.output import (
    DEFAULT_MODEL,
    SEEDREAM_MODELS,
    print_error,
    print_image_result,
    print_json,
)

SIZE_PATTERN = re.compile(r"^(1K|1\.5K|2K|3K|4K|auto|[0-9]+x[0-9]+)$")


def validate_size(_ctx: click.Context, _param: click.Parameter, value: str | None) -> str | None:
    """Validate Seedream size values from the OpenAPI pattern."""
    if value is not None and not SIZE_PATTERN.fullmatch(value):
        raise click.BadParameter("must be 1K, 1.5K, 2K, 3K, 4K, auto, or WIDTHxHEIGHT")
    return value


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SEEDREAM_MODELS),
    default=DEFAULT_MODEL,
    help="Seedream model version.",
)
@click.option(
    "-r",
    "--resolution",
    callback=validate_size,
    default=None,
    help="Output resolution (1K, 1.5K, 2K, 3K, 4K, auto, or WIDTHxHEIGHT).",
)
@click.option(
    "--sequential-image-generation",
    type=click.Choice(["auto", "disabled"]),
    default=None,
    help="Sequential image generation mode (auto or disabled).",
)
@click.option("--stream", is_flag=True, default=False, help="Stream image generation progress.")
@click.option(
    "--response-format",
    type=click.Choice(["url", "b64_json"]),
    default=None,
    help="Response format: url (default) or b64_json.",
)
@click.option(
    "--watermark/--no-watermark", default=None, help="Add AI-generated watermark (default: true)."
)
@click.option(
    "--output-format",
    type=click.Choice(["jpeg", "png"]),
    default=None,
    help="Output image file format: jpeg (default) or png. Only supported for doubao-seedream-5-0-pro-260628 and doubao-seedream-5-0-260128.",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque"]),
    default=None,
    help="Background mode for supported models.",
)
@click.option(
    "--sequential-max-images",
    type=click.IntRange(1, 15),
    default=None,
    help="Max images for sequential generation (1-15). Only used when --sequential-image-generation=auto.",
)
@click.option(
    "--optimize-prompt-mode",
    type=click.Choice(["standard", "fast"]),
    default=None,
    help="Prompt optimization mode. Only supported on doubao-seedream-5.0-lite, doubao-seedream-4.5, and doubao-seedream-4.0.",
)
@click.option(
    "--web-search",
    is_flag=True,
    default=False,
    help="Enable web search tool. Only supported for doubao-seedream-5-0-260128.",
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
    resolution: str | None,
    sequential_image_generation: str | None,
    sequential_max_images: int | None,
    optimize_prompt_mode: str | None,
    stream: bool,
    response_format: str | None,
    watermark: bool | None,
    output_format: str | None,
    background: str | None,
    web_search: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate an image from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      seedream generate "A beautiful landscape painting"

      seedream generate "A product photo" -m doubao-seedream-4-5-251128
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "sequential_image_generation": sequential_image_generation,
            "sequential_image_generation_options": {"max_images": sequential_max_images}
            if sequential_max_images is not None
            else None,
            "optimize_prompt_options": {"mode": optimize_prompt_mode}
            if optimize_prompt_mode is not None
            else None,
            "stream": stream if stream else None,
            "response_format": response_format,
            "watermark": watermark,
            "output_format": output_format,
            "background": background,
            "tools": [{"type": "web_search"}] if web_search else None,
            "callback_url": callback_url,
            "async": async_mode,
        }
        if resolution:
            payload["size"] = resolution

        result = client.generate_image(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except SeedreamError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt", required=False)
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
    type=click.Choice(SEEDREAM_MODELS),
    default=DEFAULT_MODEL,
    help="Seedream model version.",
)
@click.option(
    "--response-format",
    type=click.Choice(["url", "b64_json"]),
    default=None,
    help="Response format: url (default) or b64_json.",
)
@click.option(
    "-r",
    "--resolution",
    callback=validate_size,
    default=None,
    help="Output resolution (1K, 1.5K, 2K, 3K, 4K, auto, or WIDTHxHEIGHT).",
)
@click.option(
    "--watermark/--no-watermark", default=None, help="Add AI-generated watermark (default: true)."
)
@click.option(
    "--output-format",
    type=click.Choice(["jpeg", "png"]),
    default=None,
    help="Output image file format: jpeg (default) or png.",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque"]),
    default=None,
    help="Background mode for supported models.",
)
@click.option(
    "--layer-decomposition",
    is_flag=True,
    default=False,
    help="Enable layer decomposition for supported image inputs.",
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
    prompt: str | None,
    image_urls: tuple[str, ...],
    model: str,
    response_format: str | None,
    resolution: str | None,
    watermark: bool | None,
    output_format: str | None,
    background: str | None,
    layer_decomposition: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Edit or combine images using AI.

    PROMPT describes the desired edit. Use with one or more image URLs.
    PROMPT may be omitted when using --layer-decomposition.

    Examples:

      seedream edit "Convert to anime style" -i https://example.com/photo.jpg

      seedream edit "Virtual try-on" -i person.jpg -i shirt.jpg
    """
    client = get_client(ctx.obj.get("token"))
    if not prompt and not layer_decomposition:
        raise click.UsageError("PROMPT is required unless --layer-decomposition is used")
    if layer_decomposition and background is not None:
        raise click.UsageError("--background cannot be used with --layer-decomposition")
    try:
        result = client.edit_image(
            prompt=prompt,
            image=list(image_urls),
            model=model,
            size=resolution,
            response_format=response_format,
            watermark=watermark,
            output_format=output_format,
            background=background,
            layer_decomposition=layer_decomposition or None,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
        )
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except SeedreamError as e:
        print_error(e.message)
        raise SystemExit(1) from e

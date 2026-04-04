"""Image generation commands."""

import click

from seedream_cli.core.client import get_client
from seedream_cli.core.exceptions import SeedreamError
from seedream_cli.core.output import (
    DEFAULT_MODEL,
    RESOLUTIONS,
    SEEDREAM_MODELS,
    print_error,
    print_image_result,
    print_json,
)


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
    type=click.Choice(RESOLUTIONS),
    default=None,
    help="Output resolution.",
)
@click.option("--seed", type=int, default=None, help="Seed for reproducible generation (range: -1 to 2147483647).")
@click.option(
    "--sequential-image-generation",
    type=click.Choice(["auto", "disabled"]),
    default=None,
    help="Sequential image generation mode (auto or disabled).",
)
@click.option("--stream", is_flag=True, default=False, help="Stream image generation progress.")
@click.option("--guidance-scale", type=float, default=None, help="Prompt weight (range: 1-10).")
@click.option(
    "--response-format",
    type=str,
    default=None,
    help="Response format: url (default) or b64_json.",
)
@click.option("--watermark/--no-watermark", default=None, help="Add AI-generated watermark (default: true).")
@click.option(
    "--output-format",
    type=click.Choice(["jpeg", "png"]),
    default=None,
    help="Output image file format: jpeg (default) or png. Only supported for doubao-seedream-5-0-260128.",
)
@click.option(
    "--web-search",
    is_flag=True,
    default=False,
    help="Enable web search tool. Only supported for doubao-seedream-5-0-260128.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    resolution: str | None,
    seed: int | None,
    sequential_image_generation: str | None,
    stream: bool,
    guidance_scale: float | None,
    response_format: str | None,
    watermark: bool | None,
    output_format: str | None,
    web_search: bool,
    callback_url: str | None,
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
            "seed": seed,
            "sequential_image_generation": sequential_image_generation,
            "stream": stream if stream else None,
            "guidance_scale": guidance_scale,
            "response_format": response_format,
            "watermark": watermark,
            "output_format": output_format,
            "tools": [{"type": "web_search"}] if web_search else None,
            "callback_url": callback_url,
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
    type=click.Choice(SEEDREAM_MODELS),
    default=DEFAULT_MODEL,
    help="Seedream model version.",
)
@click.option("--seed", type=int, default=None, help="Seed for reproducible generation (range: -1 to 2147483647).")
@click.option("--guidance-scale", type=float, default=None, help="Prompt weight (range: 1-10).")
@click.option(
    "--response-format",
    type=str,
    default=None,
    help="Response format: url (default) or b64_json.",
)
@click.option("--watermark/--no-watermark", default=None, help="Add AI-generated watermark (default: true).")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edit(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    seed: int | None,
    guidance_scale: float | None,
    response_format: str | None,
    watermark: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Edit or combine images using AI.

    PROMPT describes the desired edit. Use with one or more image URLs.

    Examples:

      seedream edit "Convert to anime style" -i https://example.com/photo.jpg

      seedream edit "Virtual try-on" -i person.jpg -i shirt.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.edit_image(
            prompt=prompt,
            image=list(image_urls),
            model=model,
            seed=seed,
            guidance_scale=guidance_scale,
            response_format=response_format,
            watermark=watermark,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except SeedreamError as e:
        print_error(e.message)
        raise SystemExit(1) from e

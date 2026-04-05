"""Image generation and editing commands."""

import click

from flux_cli.core.client import get_client
from flux_cli.core.exceptions import FluxError
from flux_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_MODEL,
    FLUX_MODELS,
    print_error,
    print_image_result,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(FLUX_MODELS),
    default=DEFAULT_MODEL,
    help="Flux model to use.",
)
@click.option(
    "-s",
    "--size",
    default=None,
    help="Image size: pixels (e.g. 1024x1024) or aspect ratio (e.g. 16:9).",
)
@click.option(
    "-n",
    "--count",
    default=None,
    type=int,
    help="Number of images to generate.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    size: str | None,
    count: int | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate an image from a text prompt.

    PROMPT is a detailed description of the image to generate.

    \b
    Examples:
      flux generate "A majestic mountain at golden hour, photorealistic"
      flux generate "Cyberpunk city with neon lights" -m flux-pro-1.1
      flux generate "Minimalist logo of a phoenix" -m flux-pro-1.1-ultra -s 16:9
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "model": model,
            "size": size,
            "count": count,
            "callback_url": callback_url,
        }

        result = client.generate_image(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except FluxError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt")
@click.option(
    "--image-url",
    required=True,
    help="URL of the image to edit.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(FLUX_MODELS),
    default="flux-kontext-pro",
    help="Flux model to use (default: flux-kontext-pro).",
)
@click.option(
    "-s",
    "--size",
    default=None,
    help="Output size: pixels or aspect ratio.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edit(
    ctx: click.Context,
    prompt: str,
    image_url: str,
    model: str,
    size: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Edit an existing image with a text prompt.

    PROMPT describes the desired changes to the image.

    \b
    Examples:
      flux edit "Add sunglasses" --image-url https://example.com/photo.jpg
      flux edit "Change background to sunset" --image-url https://example.com/img.png -m flux-kontext-max
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "edit",
            "prompt": prompt,
            "image_url": image_url,
            "model": model,
            "size": size,
            "callback_url": callback_url,
        }

        result = client.edit_image(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except FluxError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("aspect-ratios")
def aspect_ratios() -> None:
    """List available aspect ratios for ultra/kontext models."""
    from rich.table import Table

    from flux_cli.core.output import console

    table = Table(title="Available Aspect Ratios")
    table.add_column("Ratio", style="bold cyan")
    table.add_column("Orientation")

    for ratio in ASPECT_RATIOS:
        w, h = ratio.split(":")
        if int(w) > int(h):
            orientation = "Landscape"
        elif int(w) < int(h):
            orientation = "Portrait"
        else:
            orientation = "Square"
        table.add_row(ratio, orientation)

    console.print(table)

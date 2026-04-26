"""Image generation commands."""

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import (
    DEFAULT_MODE,
    IMAGINE_ACTIONS,
    MIDJOURNEY_MODES,
    MIDJOURNEY_VERSIONS,
    print_error,
    print_imagine_result,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(MIDJOURNEY_MODES),
    default=DEFAULT_MODE,
    help="Generation mode: fast (default), turbo (faster, more credits), relax (slower, cheaper).",
)
@click.option(
    "--version",
    "mj_version",
    type=click.Choice(MIDJOURNEY_VERSIONS),
    default=None,
    help="Midjourney model version (5.2, 6, 6.1, 7, 8).",
)
@click.option("--translation/--no-translation", default=False, help="Auto-translate to English.")
@click.option(
    "--split/--no-split", "split_images", default=False, help="Split 2x2 grid into 4 images."
)
@click.option("--hd", is_flag=True, default=False, help="Enable HD mode (V8 only, 4x cost).")
@click.option(
    "--quality",
    default=None,
    help="Quality level. V8: '1' or '4' (ultra). Older: '.25', '.5', '1'.",
)
@click.option(
    "--style-reference/--no-style-reference",
    "style_reference",
    default=False,
    help="Prompt uses style references (--sref). V8 only, costs 4x GPU time.",
)
@click.option(
    "--moodboard/--no-moodboard",
    default=False,
    help="Prompt uses moodboard references. V8 only, costs 4x GPU time.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def imagine(
    ctx: click.Context,
    prompt: str,
    mode: str,
    mj_version: str | None,
    translation: bool,
    split_images: bool,
    hd: bool,
    quality: str | None,
    style_reference: bool,
    moodboard: bool,
    callback_url: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Generate images from a text prompt.

    Creates a 2x2 grid of 4 image variations from your description.

    \b
    Examples:
      midjourney imagine "A majestic lion at sunset, cinematic lighting"
      midjourney imagine "Cyberpunk city" --mode turbo --version 8 --hd
      midjourney imagine "水墨画" --translation
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "mode": mode,
            "action": "generate",
            "translation": translation,
            "split_images": split_images,
            "callback_url": callback_url,
            "timeout": timeout,
        }
        if mj_version is not None:
            payload["version"] = mj_version
        if hd:
            payload["hd"] = hd
        if quality is not None:
            payload["quality"] = quality
        if style_reference:
            payload["style_reference"] = style_reference
        if moodboard:
            payload["moodboard"] = moodboard

        result = client.imagine(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_imagine_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("image_id")
@click.argument(
    "action",
    type=click.Choice(
        [a for a in IMAGINE_ACTIONS if a != "generate"],
    ),
)
@click.option("--prompt", default=None, help="Prompt for variation_region action.")
@click.option("--mask", default=None, help="Base64-encoded mask for variation_region.")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(MIDJOURNEY_MODES),
    default=DEFAULT_MODE,
    help="Generation mode.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def transform(
    ctx: click.Context,
    image_id: str,
    action: str,
    prompt: str | None,
    mask: str | None,
    mode: str,
    output_json: bool,
) -> None:
    """Transform an existing image (upscale, variation, zoom, pan).

    IMAGE_ID is the image_id from a previous generation.
    ACTION is the transformation to perform.

    \b
    Examples:
      midjourney transform abc123 upscale1
      midjourney transform abc123 variation_strong
      midjourney transform abc123 zoom_out_2x
      midjourney transform abc123 pan_left
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": action,
            "image_id": image_id,
            "mode": mode,
        }
        if prompt:
            payload["prompt"] = prompt
        if mask:
            payload["mask"] = mask

        result = client.imagine(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_imagine_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("image_urls", nargs=-1, required=True)
@click.option("--prompt", default="", help="Description of how to blend the images.")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(MIDJOURNEY_MODES),
    default=DEFAULT_MODE,
    help="Generation mode.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def blend(
    ctx: click.Context,
    image_urls: tuple[str, ...],
    prompt: str,
    mode: str,
    output_json: bool,
) -> None:
    """Blend multiple images together (2-5 images).

    IMAGE_URLS are space-separated URLs of images to blend.

    \b
    Examples:
      midjourney blend https://example.com/bear.jpg https://example.com/chainsaw.jpg
      midjourney blend img1.jpg img2.jpg --prompt "The bear holds the chainsaw"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        full_prompt = " ".join(image_urls)
        if prompt:
            full_prompt += f" {prompt}"

        result = client.imagine(prompt=full_prompt, mode=mode, action="generate")
        if output_json:
            print_json(result)
        else:
            print_imagine_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

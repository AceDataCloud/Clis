"""Image editing commands."""

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import (
    DEFAULT_MODE,
    MIDJOURNEY_MODES,
    print_edit_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("image_url")
@click.argument("prompt")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(MIDJOURNEY_MODES),
    default=DEFAULT_MODE,
    help="Generation mode.",
)
@click.option(
    "--split/--no-split", "split_images", default=False, help="Split result into separate images."
)
@click.option("--mask", default=None, help="Base64-encoded mask. White areas = regions to edit.")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edit(
    ctx: click.Context,
    image_url: str,
    prompt: str,
    mode: str,
    split_images: bool,
    mask: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Edit an existing image with a text prompt.

    IMAGE_URL is the URL of the image to edit.
    PROMPT describes how to modify the image.

    \b
    Examples:
      midjourney edit https://example.com/photo.jpg "Add a sunset background"
      midjourney edit img.jpg "Make it a watercolor painting" --mode turbo
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "image_url": image_url,
            "prompt": prompt,
            "mode": mode,
            "split_images": split_images,
            "callback_url": callback_url,
        }
        if mask:
            payload["mask"] = mask

        result = client.edit(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_edit_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("image_url")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def describe(
    ctx: click.Context,
    image_url: str,
    output_json: bool,
) -> None:
    """Get AI descriptions of an image (reverse prompt engineering).

    Returns 4 alternative text descriptions that could recreate a similar image.

    \b
    Examples:
      midjourney describe https://example.com/photo.jpg
      midjourney describe photo.jpg --json
    """
    client = get_client(ctx.obj.get("token"))
    try:
        from midjourney_cli.core.output import print_describe_result

        result = client.describe(image_url=image_url)
        if output_json:
            print_json(result)
        else:
            print_describe_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("content")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def translate(
    ctx: click.Context,
    content: str,
    output_json: bool,
) -> None:
    """Translate Chinese text to English for Midjourney prompts.

    CONTENT is the Chinese text to translate.

    \b
    Examples:
      midjourney translate "一只猫坐在桌子上"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        from midjourney_cli.core.output import print_translate_result

        result = client.translate(content=content)
        if output_json:
            print_json(result)
        else:
            print_translate_result(result)
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

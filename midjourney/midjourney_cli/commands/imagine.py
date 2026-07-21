"""Imagine (image generation) command."""

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import (
    DEFAULT_IMAGINE_MODE,
    IMAGINE_MODES,
    print_error,
    print_json,
    print_result,
)


@click.command()
@click.argument("prompt", required=False)
@click.option("--action", default="generate", help="Action to perform (default: generate).")
@click.option(
    "--mode",
    type=click.Choice(IMAGINE_MODES),
    default=DEFAULT_IMAGINE_MODE,
    help="Generation mode: fast, relax, or turbo.",
)
@click.option("--image-id", default=None, help="Image ID for reference.")
@click.option("--mask", default=None, help="Mask for the generation.")
@click.option(
    "--translation/--no-translation",
    default=False,
    help="Enable prompt translation.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option(
    "--split-images/--no-split-images",
    default=False,
    help="Split generated images into individual files.",
)
@click.option("--version", default=None, help="Midjourney version to use.")
@click.option("--hd/--no-hd", default=False, help="Enable HD generation.")
@click.option("--quality", default=None, help="Quality setting.")
@click.option(
    "--style-reference/--no-style-reference",
    default=False,
    help="Enable style reference.",
)
@click.option("--moodboard/--no-moodboard", default=False, help="Enable moodboard mode.")
@click.option(
    "--timeout", default=480, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def imagine(
    ctx: click.Context,
    prompt: str | None,
    action: str,
    mode: str,
    image_id: str | None,
    mask: str | None,
    translation: bool,
    callback_url: str | None,
    async_mode: bool,
    split_images: bool,
    version: str | None,
    hd: bool,
    quality: str | None,
    style_reference: bool,
    moodboard: bool,
    timeout: int,
    output_json: bool,
) -> None:
    """Generate an image with Midjourney.

    PROMPT is a description of the image to generate.

    Examples:

      midjourney imagine "A beautiful sunset over the ocean"

      midjourney imagine "A futuristic cityscape" --mode turbo --hd
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": action,
            "prompt": prompt,
            "mode": mode,
            "image_id": image_id,
            "mask": mask,
            "translation": translation if translation else None,
            "callback_url": callback_url,
            "async": async_mode if async_mode else None,
            "split_images": split_images if split_images else None,
            "version": version,
            "hd": hd if hd else None,
            "quality": quality,
            "style_reference": style_reference if style_reference else None,
            "moodboard": moodboard if moodboard else None,
            "timeout": timeout,
        }
        result = client.imagine(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_result(result, title="Imagine Result")
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

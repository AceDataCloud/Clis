"""Edits (image editing) command."""

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import IMAGINE_MODES, print_error, print_json, print_result


@click.command()
@click.option("--action", default="generate", help="Action to perform (default: generate).")
@click.option(
    "--mode",
    type=click.Choice(IMAGINE_MODES),
    default=None,
    help="Generation mode: fast, relax, or turbo.",
)
@click.option("--prompt", default=None, help="Editing prompt.")
@click.option("--image-url", default=None, help="URL of the image to edit.")
@click.option("--mask", default=None, help="Mask for the edit.")
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
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def edits(
    ctx: click.Context,
    action: str,
    mode: str | None,
    prompt: str | None,
    image_url: str | None,
    mask: str | None,
    callback_url: str | None,
    async_mode: bool,
    split_images: bool,
    output_json: bool,
) -> None:
    """Edit an image with Midjourney.

    Examples:

      midjourney edits --image-url https://example.com/photo.jpg --prompt "Add mountains"

      midjourney edits --image-url https://example.com/photo.jpg --action vary --mode fast
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": action,
            "mode": mode,
            "prompt": prompt,
            "image_url": image_url,
            "mask": mask,
            "callback_url": callback_url,
            "async": async_mode if async_mode else None,
            "split_images": split_images if split_images else None,
        }
        result = client.edits(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_result(result, title="Edits Result")
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

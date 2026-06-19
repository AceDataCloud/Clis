"""Video generation commands."""

import click

from dreamina_cli.core.client import get_client
from dreamina_cli.core.exceptions import DreaminaError
from dreamina_cli.core.output import (
    DEFAULT_MODEL,
    DREAMINA_MODELS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.option(
    "--image-url",
    required=True,
    help="URL of the portrait image.",
)
@click.option(
    "--audio-url",
    required=True,
    help="URL of the audio file.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(DREAMINA_MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Dreamina model to use.",
)
@click.option(
    "--prompt",
    default=None,
    help="Optional text prompt to guide the video generation.",
)
@click.option(
    "--mask-url",
    multiple=True,
    default=None,
    help="URL(s) of mask image(s) (repeatable).",
)
@click.option(
    "--callback-url",
    default=None,
    help="Webhook callback URL.",
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
def generate(
    ctx: click.Context,
    image_url: str,
    audio_url: str,
    model: str,
    prompt: str | None,
    mask_url: tuple[str, ...],
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a talking-head video from an image and audio.

    \b
    Examples:
      dreamina generate --image-url https://example.com/portrait.jpg \\
                        --audio-url https://example.com/speech.mp3
      dreamina generate --image-url https://example.com/portrait.jpg \\
                        --audio-url https://example.com/speech.mp3 \\
                        --prompt "Smiling face" --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "model": model,
        "image_url": image_url,
        "audio_url": audio_url,
    }
    if prompt is not None:
        payload["prompt"] = prompt
    if mask_url:
        payload["mask_url"] = list(mask_url)
    if callback_url is not None:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate_video(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except DreaminaError as e:
        print_error(e.message)
        raise SystemExit(1) from e

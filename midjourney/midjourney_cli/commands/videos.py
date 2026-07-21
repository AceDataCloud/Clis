"""Videos (video generation) command."""

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import (
    VIDEO_ACTIONS,
    VIDEO_MODES,
    VIDEO_RESOLUTIONS,
    print_error,
    print_json,
    print_result,
)


@click.command()
@click.option(
    "--action",
    type=click.Choice(VIDEO_ACTIONS),
    default=None,
    help="Video action: generate or extend.",
)
@click.option(
    "--mode",
    type=click.Choice(VIDEO_MODES),
    default=None,
    help="Generation mode: fast or turbo.",
)
@click.option(
    "--resolution",
    type=click.Choice(VIDEO_RESOLUTIONS),
    default=None,
    help="Video resolution: 480p or 720p.",
)
@click.option("--prompt", default=None, help="Video generation prompt.")
@click.option("--video-id", default=None, help="Video ID for extension.")
@click.option("--video-index", default=None, type=int, help="Video index.")
@click.option("--loop/--no-loop", default=None, help="Enable loop mode.")
@click.option("--image-url", default=None, help="Reference image URL.")
@click.option("--end-image-url", default=None, help="End frame image URL.")
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
def videos(
    ctx: click.Context,
    action: str | None,
    mode: str | None,
    resolution: str | None,
    prompt: str | None,
    video_id: str | None,
    video_index: int | None,
    loop: bool | None,
    image_url: str | None,
    end_image_url: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video with Midjourney.

    Examples:

      midjourney videos --prompt "A flowing river" --action generate

      midjourney videos --video-id abc123 --action extend --mode turbo

      midjourney videos --image-url https://example.com/photo.jpg --action generate --resolution 720p
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": action,
            "mode": mode,
            "resolution": resolution,
            "prompt": prompt,
            "video_id": video_id,
            "video_index": video_index,
            "loop": loop,
            "image_url": image_url,
            "end_image_url": end_image_url,
            "callback_url": callback_url,
            "async": async_mode if async_mode else None,
        }
        result = client.videos(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_result(result, title="Videos Result")
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

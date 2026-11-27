"""Video generation commands."""

import click

from adc_cli.core.client import get_client
from adc_cli.core.exceptions import AdcError
from adc_cli.core.output import print_error, print_json, print_media_response, print_result


@click.command()
@click.argument("prompt")
@click.option(
    "--service",
    type=click.Choice(["luma", "veo", "seedance", "kling"]),
    default="luma",
    help="Video generation service to use.",
)
@click.option("-a", "--aspect-ratio", default=None, help="Aspect ratio (e.g. 16:9).")
@click.option("--loop", is_flag=True, default=False, help="Enable loop.")
@click.option("-m", "--model", help="Kling model ID, passed exactly as supplied.")
@click.option("--mode", help="Kling generation mode, for example std, pro or 4k.")
@click.option("--duration", type=float, help="Kling video duration in seconds.")
@click.option("--image-url", help="Reference image URL to animate with Kling.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def video(
    ctx: click.Context,
    prompt: str,
    service: str,
    aspect_ratio: str | None,
    loop: bool,
    model: str | None,
    mode: str | None,
    duration: float | None,
    image_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video using AI.

    PROMPT describes the video to generate.

    \b
    Examples:
      adc video "A cinematic sunset over the ocean"
      adc video "Cat playing with yarn" --service luma --loop
      adc video "A rocket launching" --service seedance
    """
    if service != "kling" and any(
        value is not None for value in (model, mode, duration, image_url)
    ):
        raise click.UsageError(
            "--model, --mode, --duration and --image-url are available with --service kling."
        )
    if service == "kling" and loop:
        raise click.UsageError("Kling does not accept --loop.")
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "loop": loop,
        }

        if service == "kling":
            result = client.request(
                "/kling/videos",
                {
                    "action": "image2video" if image_url else "text2video",
                    "prompt": prompt,
                    "model": model,
                    "mode": mode,
                    "aspect_ratio": aspect_ratio,
                    "duration": duration,
                    "start_image_url": image_url,
                    "async": True,
                },
            )
        elif service == "luma":
            result = client.luma_video(**payload)  # type: ignore[arg-type]
        else:
            result = client.request(
                f"/{service}/videos",
                client._with_async_callback(payload),  # noqa: SLF001
            )

        if output_json:
            print_json(result)
        elif service == "kling":
            print_media_response(result)
        else:
            print_result(result, "Video Result")
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e

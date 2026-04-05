"""Video generation commands."""

import click

from adc_cli.core.client import get_client
from adc_cli.core.exceptions import AdcError
from adc_cli.core.output import print_error, print_json, print_result


@click.command()
@click.argument("prompt")
@click.option(
    "--service",
    type=click.Choice(["luma", "sora", "veo", "seedance"]),
    default="luma",
    help="Video generation service to use.",
)
@click.option("-a", "--aspect-ratio", default=None, help="Aspect ratio (e.g. 16:9).")
@click.option("--loop", is_flag=True, default=False, help="Enable loop.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def video(
    ctx: click.Context,
    prompt: str,
    service: str,
    aspect_ratio: str | None,
    loop: bool,
    output_json: bool,
) -> None:
    """Generate a video using AI.

    PROMPT describes the video to generate.

    \b
    Examples:
      adc video "A cinematic sunset over the ocean"
      adc video "Cat playing with yarn" --service luma --loop
      adc video "A rocket launching" --service sora
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "loop": loop,
        }

        if service == "luma":
            result = client.luma_video(**payload)  # type: ignore[arg-type]
        elif service == "sora":
            result = client.sora_video(**payload)  # type: ignore[arg-type]
        else:
            result = client.request(
                f"/{service}/videos",
                client._with_async_callback(payload),  # noqa: SLF001
            )

        if output_json:
            print_json(result)
        else:
            print_result(result, "Video Result")
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Image generation commands."""

import click

from adc_cli.core.client import get_client
from adc_cli.core.exceptions import AdcError
from adc_cli.core.output import print_error, print_json, print_result


@click.command()
@click.argument("prompt")
@click.option(
    "--service",
    type=click.Choice(["flux", "midjourney", "seedream", "nanobanana"]),
    default="flux",
    help="Image generation service to use.",
)
@click.option("-m", "--model", default=None, help="Model name (service-specific).")
@click.option("-s", "--size", default=None, help="Image size or aspect ratio.")
@click.option("-n", "--count", default=None, type=int, help="Number of images.")
@click.option("--image-url", default=None, help="Source image URL (for editing).")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image(
    ctx: click.Context,
    prompt: str,
    service: str,
    model: str | None,
    size: str | None,
    count: int | None,
    image_url: str | None,
    output_json: bool,
) -> None:
    """Generate or edit an image using AI.

    PROMPT describes the image to generate or changes to make.

    \b
    Examples:
      adc image "A sunset over mountains, photorealistic"
      adc image "Cyberpunk city" --service midjourney
      adc image "Add sunglasses" --image-url https://example.com/photo.jpg
      adc image "Logo design" --service flux -m flux-pro-1.1-ultra -s 16:9
    """
    client = get_client(ctx.obj.get("token"))
    try:
        if service == "flux":
            action = "edit" if image_url else "generate"
            payload: dict[str, object] = {
                "action": action,
                "prompt": prompt,
                "model": model or ("flux-kontext-pro" if image_url else "flux-dev"),
                "size": size,
                "count": count,
                "image_url": image_url,
            }
            result = client.flux_image(**payload)  # type: ignore[arg-type]
        elif service == "midjourney":
            payload = {
                "prompt": prompt,
                "size": size,
                "version": model,
            }
            result = client.midjourney_imagine(**payload)  # type: ignore[arg-type]
        else:
            # seedream, nanobanana — generic image endpoint
            payload = {
                "action": "generate",
                "prompt": prompt,
                "model": model,
                "size": size,
            }
            result = client.request(
                f"/{service}/images",
                client._with_async_callback(payload),  # noqa: SLF001
            )

        if output_json:
            print_json(result)
        else:
            print_result(result, "Image Result")
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e

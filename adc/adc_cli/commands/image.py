"""Image generation commands."""

import click

from adc_cli.core.client import get_client
from adc_cli.core.exceptions import AdcError
from adc_cli.core.output import print_error, print_json, print_media_response, print_result


@click.command()
@click.argument("prompt")
@click.option(
    "--service",
    type=click.Choice(["flux", "seedream", "nano-banana", "nanobanana", "gpt-image", "openai"]),
    default="flux",
    help="Image generation service to use.",
)
@click.option("-m", "--model", default=None, help="Model name (service-specific).")
@click.option("-s", "--size", default=None, help="Image size or aspect ratio.")
@click.option("-n", "--count", default=None, type=int, help="Number of images.")
@click.option("--image-url", default=None, help="Source image URL (for editing).")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    help="Request a task ID for GPT Image. Other image services submit asynchronously.",
)
@click.option(
    "--response-format", type=click.Choice(["url", "b64_json"]), help="GPT Image result format."
)
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
    async_mode: bool,
    response_format: str | None,
    output_json: bool,
) -> None:
    """Generate or edit an image using AI.

    PROMPT describes the image to generate or changes to make.

    \b
    Examples:
      adc image "A sunset over mountains, photorealistic"
      adc image "Add sunglasses" --image-url https://example.com/photo.jpg
      adc image "Logo design" --service flux -m flux-pro-1.1-ultra -s 16:9
    """
    gpt_image = service in {"gpt-image", "openai"}
    if gpt_image and not model:
        raise click.UsageError("Choose a GPT Image model with --model, for example gpt-image-2.")
    if response_format and not gpt_image:
        raise click.UsageError("--response-format is available with --service gpt-image.")
    client = get_client(ctx.obj.get("token"))
    try:
        if gpt_image:
            path = "/openai/images/edits" if image_url else "/openai/images/generations"
            result = client.request(
                path,
                {
                    "model": model,
                    "prompt": prompt,
                    "image": image_url,
                    "size": size,
                    "n": count,
                    "response_format": response_format,
                    "async": True if async_mode else None,
                },
            )
        elif service == "flux":
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
        elif service in {"nano-banana", "nanobanana"}:
            payload = {
                "action": "edit" if image_url else "generate",
                "prompt": prompt,
                "model": model,
                "count": count,
                "image_urls": [image_url] if image_url else None,
            }
            if size:
                payload["aspect_ratio" if ":" in size else "resolution"] = size
            result = client.request("/nano-banana/images", client._with_async_callback(payload))
        else:
            payload = {
                "action": "edit" if image_url else "generate",
                "prompt": prompt,
                "model": model,
                "size": size,
                "image": [image_url] if image_url else None,
            }
            result = client.request("/seedream/images", client._with_async_callback(payload))

        if output_json:
            print_json(result)
        elif gpt_image:
            print_media_response(result)
        else:
            print_result(result, "Image Result")
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e

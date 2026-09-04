"""Image generation commands."""

import click

from seedream_cli.core.client import get_client
from seedream_cli.core.exceptions import SeedreamError
from seedream_cli.core.output import (
    DEFAULT_MODEL,
    SEEDREAM_MODELS,
    print_error,
    print_image_result,
    print_json,
)


class SizeType(click.ParamType):
    """Accept current presets or explicit WIDTHxHEIGHT dimensions."""

    name = "size"

    def convert(
        self, value: object, param: click.Parameter | None, ctx: click.Context | None
    ) -> str | None:
        if value is None:
            return None
        text = str(value)
        import re

        if text in {"1K", "1.5K", "2K", "3K", "4K", "auto"} or re.fullmatch(r"[0-9]+x[0-9]+", text):
            return text
        self.fail(f"{text!r} is not a supported preset or WIDTHxHEIGHT size", param, ctx)


SIZE = SizeType()


def _common_result(result: dict, output_json: bool) -> None:
    if output_json:
        print_json(result)
    else:
        print_image_result(result)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SEEDREAM_MODELS),
    default=DEFAULT_MODEL,
    help="Seedream model version.",
)
@click.option(
    "-r", "--resolution", type=SIZE, default=None, help="Model-specific preset or WIDTHxHEIGHT."
)
@click.option(
    "--sequential-image-generation", type=click.Choice(["auto", "disabled"]), default=None
)
@click.option("--sequential-max-images", type=click.IntRange(1, 15), default=None)
@click.option(
    "--stream", is_flag=True, default=False, help="Stream normalized NDJSON image events."
)
@click.option("--response-format", type=click.Choice(["url", "b64_json"]), default=None)
@click.option("--watermark/--no-watermark", default=None)
@click.option("--output-format", type=click.Choice(["jpeg", "png"]), default=None)
@click.option("--optimize-prompt-mode", type=click.Choice(["standard", "fast"]), default=None)
@click.option(
    "--web-search", is_flag=True, default=False, help="Enable web search on Seedream 5.0 Lite."
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously and return a task id.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    resolution: str | None,
    sequential_image_generation: str | None,
    sequential_max_images: int | None,
    stream: bool,
    response_format: str | None,
    watermark: bool | None,
    output_format: str | None,
    optimize_prompt_mode: str | None,
    web_search: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate an image from PROMPT."""
    if stream and (async_mode or callback_url):
        raise click.UsageError("--stream cannot be combined with --async or --callback-url")
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object | None] = {
        "prompt": prompt,
        "model": model,
        "size": resolution,
        "sequential_image_generation": sequential_image_generation,
        "sequential_image_generation_options": {"max_images": sequential_max_images}
        if sequential_max_images is not None
        else None,
        "response_format": response_format,
        "watermark": watermark,
        "output_format": output_format,
        "optimize_prompt_options": {"mode": optimize_prompt_mode} if optimize_prompt_mode else None,
        "tools": [{"type": "web_search"}] if web_search else None,
        "callback_url": callback_url,
        "async": async_mode,
    }
    try:
        if stream:
            payload["stream"] = True
            for event in client.stream_images(**payload):
                _common_result(event, output_json)
        else:
            _common_result(client.generate_image(**payload), output_json)  # type: ignore[arg-type]
    except SeedreamError as error:
        print_error(error.message)
        raise SystemExit(1) from error


@click.command()
@click.argument("prompt")
@click.option(
    "-i", "--image-url", "image_urls", required=True, multiple=True, help="Image URL(s) to edit."
)
@click.option("-m", "--model", type=click.Choice(SEEDREAM_MODELS), default=DEFAULT_MODEL)
@click.option(
    "-r", "--resolution", type=SIZE, default=None, help="Model-specific preset or WIDTHxHEIGHT."
)
@click.option("--response-format", type=click.Choice(["url", "b64_json"]), default=None)
@click.option("--watermark/--no-watermark", default=None)
@click.option("--output-format", type=click.Choice(["jpeg", "png"]), default=None)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque"]),
    default=None,
    help="Seedream 5.0 Pro background mode.",
)
@click.option("--optimize-prompt-mode", type=click.Choice(["standard", "fast"]), default=None)
@click.option("--callback-url", default=None)
@click.option("--async", "async_mode", is_flag=True, default=False)
@click.option("--json", "output_json", is_flag=True)
@click.pass_context
def edit(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    resolution: str | None,
    response_format: str | None,
    watermark: bool | None,
    output_format: str | None,
    background: str | None,
    optimize_prompt_mode: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Edit or combine images according to PROMPT."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.edit_image(
            prompt=prompt,
            image=list(image_urls),
            model=model,
            size=resolution,
            response_format=response_format,
            watermark=watermark,
            output_format=output_format,
            background=background,
            optimize_prompt_options={"mode": optimize_prompt_mode}
            if optimize_prompt_mode
            else None,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
        )
        _common_result(result, output_json)
    except SeedreamError as error:
        print_error(error.message)
        raise SystemExit(1) from error


@click.command()
@click.argument("image_url")
@click.option(
    "--prompt",
    default=None,
    help="Elements to split; omit for automatic decomposition. Supports <bbox>.",
)
@click.option("-r", "--resolution", type=click.Choice(["auto", "1K", "1.5K", "2K"]), default="auto")
@click.option(
    "--output-format",
    type=click.Choice(["jpeg", "png"]),
    default="jpeg",
    help="Base image format; layers are PNG.",
)
@click.option("--watermark/--no-watermark", default=True)
@click.option("--callback-url", default=None)
@click.option("--async", "async_mode", is_flag=True, default=False)
@click.option("--json", "output_json", is_flag=True)
@click.pass_context
def decompose(
    ctx: click.Context,
    image_url: str,
    prompt: str | None,
    resolution: str,
    output_format: str,
    watermark: bool,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Split IMAGE_URL into a base image and editable transparent layers."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.edit_image(
            model="doubao-seedream-5-0-pro-260628",
            image=image_url,
            prompt=prompt,
            size=resolution,
            output_format=output_format,
            watermark=watermark,
            layer_decomposition=True,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
        )
        _common_result(result, output_json)
    except SeedreamError as error:
        print_error(error.message)
        raise SystemExit(1) from error

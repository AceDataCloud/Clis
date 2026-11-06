"""Image generation and editing commands."""

import base64
import re
from pathlib import Path

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_IMAGE_MODEL,
    IMAGE_MODELS,
    print_error,
    print_image_result,
    print_json,
)

_SIZE_PATTERN = re.compile(r"^(auto|\d+x\d+)$")


def _validate_size_format(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> str | None:
    """Validate that size matches 'auto' or 'WIDTHxHEIGHT' pattern."""
    if value is not None and not _SIZE_PATTERN.match(value):
        raise click.BadParameter(
            f"'{value}' is not a valid size. Use 'auto' or 'WIDTHxHEIGHT' format (e.g. 1024x1024).",
            ctx=ctx,
            param=param,
        )
    return value


def _validate_quality(model: str, quality: str | None) -> None:
    base_model = model.removesuffix(":official").removesuffix(":reverse")
    if quality in {"xhigh", "max"} and base_model not in {
        "gpt-image-2.5-flare",
        "gpt-image-2.6-flare",
        "gpt-image-2.5-sunburst",
        "gpt-image-2.6-sunburst",
    }:
        raise click.BadParameter(
            "xhigh and max require GPT Image 2.5 or 2.6 Flare/Sunburst "
            "(including :reverse and :official variants).",
            param_hint="--quality",
        )


_GIF_MODELS = {
    "gpt-image-2.6-flare",
    "gpt-image-2.6-flare:reverse",
    "gpt-image-2.6-flare:official",
    "gpt-image-2.6-sunburst",
    "gpt-image-2.6-sunburst:reverse",
    "gpt-image-2.6-sunburst:official",
}


def _validate_gif_options(
    model: str, output_format: str | None, frame_count: int | None, frame_duration_ms: int | None
) -> None:
    if output_format == "gif" and model not in _GIF_MODELS:
        raise click.BadParameter(
            "GIF requires GPT Image 2.6 Flare/Sunburst (standard/reverse/official).",
            param_hint="--output-format",
        )
    if output_format != "gif" and (frame_count is not None or frame_duration_ms is not None):
        raise click.BadParameter(
            "Frame controls require --output-format gif.", param_hint="--output-format"
        )


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(IMAGE_MODELS),
    default=DEFAULT_IMAGE_MODEL,
    show_default=True,
    help="Image generation model to use; :official GPT Image variants use actual-token billing.",
)
@click.option(
    "-n",
    "--count",
    default=None,
    type=click.IntRange(1, 10),
    help="Number of images to generate (1-10).",
)
@click.option(
    "-s",
    "--size",
    default=None,
    callback=_validate_size_format,
    is_eager=False,
    help=(
        "Size of the generated image as WIDTHxHEIGHT or 'auto'. "
        "GPT Image 2/2.5/2.6 accepts WIDTHxHEIGHT with multiples of 16, max side 3840, 655360–8294400 pixels, and aspect ratio up to 3:1. "
        "dall-e-3: 1024x1024, 1792x1024, 1024x1792. "
        "dall-e-2: 256x256, 512x512, 1024x1024."
    ),
)
@click.option(
    "--complexity",
    type=click.Choice(["low", "medium", "high"]),
    default=None,
    help="GPT Image 2.6 planning complexity; model default high.",
)
@click.option(
    "--quality",
    type=click.Choice(["auto", "high", "medium", "low", "xhigh", "max", "hd", "standard"]),
    default=None,
    help=(
        "Image quality; xhigh/max only for GPT Image 2.5/2.6 Flare and "
        "Sunburst (including :reverse and :official)."
    ),
)
@click.option(
    "--style",
    type=click.Choice(["vivid", "natural"]),
    default=None,
    help="Style for dall-e-3: vivid or natural.",
)
@click.option(
    "--output-format",
    type=click.Choice(["png", "jpeg", "webp", "gif"]),
    default=None,
    help="PNG/JPEG/WebP, or GIF for all GPT Image 2.6 variants. GIF defaults to a 512 preview; use static formats for 4K.",
)
@click.option(
    "--frame-count",
    type=click.IntRange(min=2, max=16),
    default=None,
    help="GIF-only frame count; API default is 9.",
)
@click.option(
    "--frame-duration-ms",
    type=click.IntRange(min=20, max=655350),
    default=None,
    help="GIF-only frame duration in milliseconds; API default is 200.",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque", "auto"]),
    default=None,
    help="Background transparency for GPT image models.",
)
@click.option(
    "--moderation",
    type=click.Choice(["low", "auto"]),
    default=None,
    help="Content-moderation level for GPT image models.",
)
@click.option(
    "--output-compression",
    default=None,
    type=click.IntRange(0, 100),
    help="Compression level (0-100) for webp/jpeg output.",
)
@click.option(
    "--partial-images",
    default=None,
    type=click.IntRange(0, 3),
    help="Number of partial images to emit during streaming (0-3).",
)
@click.option(
    "--response-format",
    type=click.Choice(["url", "b64_json"]),
    default=None,
    help="Format for dall-e image responses.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async image generation.",
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
def image(
    ctx: click.Context,
    prompt: str,
    model: str,
    count: int | None,
    size: str | None,
    quality: str | None,
    complexity: str | None,
    style: str | None,
    output_format: str | None,
    frame_count: int | None,
    frame_duration_ms: int | None,
    background: str | None,
    moderation: str | None,
    output_compression: int | None,
    partial_images: int | None,
    response_format: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate an image from a text prompt.

    PROMPT is the text description of the desired image.

    \b
    Examples:
      openai-cli image "A futuristic city skyline at night"
      openai-cli image "Portrait of a cat" -m gpt-image-1 --quality high
      openai-cli image "Abstract art" --size 1792x1024 --style vivid
    """
    _validate_quality(model, quality)
    if complexity is not None and model not in _GIF_MODELS:
        raise click.BadParameter("complexity requires GPT Image 2.6.", param_hint="--complexity")
    if output_format == "gif" and (output_compression is not None or partial_images):
        raise click.UsageError("GIF does not support compression or partial images.")
    _validate_gif_options(model, output_format, frame_count, frame_duration_ms)
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "prompt": prompt,
        "model": model,
        "n": count,
        "size": size,
        "quality": quality,
        "complexity": complexity,
        "style": style,
        "output_format": output_format,
        "frame_count": frame_count,
        "frame_duration_ms": frame_duration_ms,
        "background": background,
        "moderation": moderation,
        "output_compression": output_compression,
        "partial_images": partial_images,
        "response_format": response_format,
        "callback_url": callback_url,
        "async": async_mode,
    }

    try:
        result = client.image_generations(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt")
@click.option(
    "--image-url",
    multiple=True,
    help="Reference image URL to edit (repeat up to 16 times).",
)
@click.option(
    "--image-file",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Reference image file to upload for editing (repeat up to 16 times).",
)
@click.option(
    "--markup-url",
    default=None,
    help="Transparent PNG annotation URL for GPT Image 2.6 static edits.",
)
@click.option(
    "--markup-file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Transparent PNG annotation matching the first reference image.",
)
@click.option(
    "--mask-file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Optional mask image file for uploaded image edits.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(IMAGE_MODELS),
    default=DEFAULT_IMAGE_MODEL,
    show_default=True,
    help="Image editing model to use; :official GPT Image variants use actual-token billing.",
)
@click.option(
    "-n",
    "--count",
    default=None,
    type=click.IntRange(1, 10),
    help="Number of images to generate (1-10).",
)
@click.option(
    "-s",
    "--size",
    default=None,
    callback=_validate_size_format,
    is_eager=False,
    help=(
        "Size of the output image as WIDTHxHEIGHT or 'auto'. "
        "GPT Image 2/2.5/2.6 accepts WIDTHxHEIGHT with multiples of 16, max side 3840, 655360–8294400 pixels, and aspect ratio up to 3:1. "
        "dall-e-3: 1024x1024, 1792x1024, 1024x1792. "
        "dall-e-2: 256x256, 512x512, 1024x1024."
    ),
)
@click.option(
    "--complexity",
    type=click.Choice(["low", "medium", "high"]),
    default=None,
    help="GPT Image 2.6 planning complexity; model default high.",
)
@click.option(
    "--quality",
    type=click.Choice(["auto", "high", "medium", "low", "xhigh", "max", "standard"]),
    default=None,
    help=(
        "Image quality; xhigh/max only for GPT Image 2.5/2.6 Flare and "
        "Sunburst (including :reverse and :official)."
    ),
)
@click.option(
    "--output-format",
    type=click.Choice(["png", "jpeg", "webp", "gif"]),
    default=None,
    help="PNG/JPEG/WebP, or GIF for all GPT Image 2.6 variants. GIF defaults to a 512 preview; use static formats for 4K.",
)
@click.option(
    "--frame-count",
    type=click.IntRange(min=2, max=16),
    default=None,
    help="GIF-only frame count; API default is 9.",
)
@click.option(
    "--frame-duration-ms",
    type=click.IntRange(min=20, max=655350),
    default=None,
    help="GIF-only frame duration in milliseconds; API default is 200.",
)
@click.option(
    "--background",
    type=click.Choice(["transparent", "opaque", "auto"]),
    default=None,
    help="Background transparency for GPT image models.",
)
@click.option(
    "--input-fidelity",
    type=click.Choice(["high", "low"]),
    default=None,
    help="How strongly to match input style/features (GPT image models only).",
)
@click.option(
    "--output-compression",
    default=None,
    type=click.IntRange(0, 100),
    help="Compression level (0-100) for webp/jpeg output.",
)
@click.option(
    "--partial-images",
    default=None,
    type=click.IntRange(0, 3),
    help="Number of partial images to emit during streaming (0-3).",
)
@click.option(
    "--response-format",
    type=click.Choice(["url", "b64_json"]),
    default=None,
    help="Response format: url or b64_json.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async image editing.",
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
def edit(
    ctx: click.Context,
    prompt: str,
    image_url: tuple[str, ...],
    image_file: tuple[str, ...],
    mask_file: str | None,
    markup_url: str | None,
    markup_file: str | None,
    model: str,
    count: int | None,
    size: str | None,
    quality: str | None,
    complexity: str | None,
    output_format: str | None,
    frame_count: int | None,
    frame_duration_ms: int | None,
    background: str | None,
    input_fidelity: str | None,
    output_compression: int | None,
    partial_images: int | None,
    response_format: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Edit an image using a text prompt.

    PROMPT describes the changes to make to the reference image.

    \b
    Examples:
      openai-cli edit "Add a rainbow" --image-url https://example.com/photo.jpg
      openai-cli edit "Change background to forest" --image-url https://example.com/pic.jpg -m gpt-image-1
      openai-cli edit "Remove background" --image-file photo.png --mask-file mask.png
    """
    _validate_quality(model, quality)
    if complexity is not None and model not in _GIF_MODELS:
        raise click.BadParameter("complexity requires GPT Image 2.6.", param_hint="--complexity")
    if output_format == "gif" and (output_compression is not None or partial_images):
        raise click.UsageError("GIF does not support compression or partial images.")
    _validate_gif_options(model, output_format, frame_count, frame_duration_ms)
    if markup_url and markup_file:
        raise click.UsageError("Use either --markup-url or --markup-file, not both.")
    if (markup_url or markup_file) and (
        model not in _GIF_MODELS or output_format == "gif" or mask_file
    ):
        raise click.UsageError("Markup requires a GPT Image 2.6 static edit without a mask.")
    if output_format == "gif" and mask_file:
        raise click.UsageError("GIF does not support masks.")
    if not image_url and not image_file:
        raise click.UsageError("Provide at least one of --image-url or --image-file.")
    if image_url and image_file:
        raise click.UsageError("Use either --image-url or --image-file, not both.")
    if image_url and (mask_file or partial_images is not None):
        raise click.UsageError("--mask-file and --partial-images require --image-file.")
    if len(image_url) > 16:
        raise click.UsageError("Provide at most 16 --image-url options.")
    if len(image_file) > 16:
        raise click.UsageError("Provide at most 16 --image-file options.")

    client = get_client(ctx.obj.get("token"))
    if image_file:
        fields: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "n": count,
            "size": size,
            "quality": quality,
            "complexity": complexity,
            "output_format": output_format,
            "frame_count": frame_count,
            "frame_duration_ms": frame_duration_ms,
            "background": background,
            "input_fidelity": input_fidelity,
            "output_compression": output_compression,
            "partial_images": partial_images,
            "response_format": response_format,
            "callback_url": callback_url,
            "async": async_mode,
        }
        files: list[tuple[str, object]] = [
            ("image", (Path(path).name, Path(path).read_bytes(), "application/octet-stream"))
            for path in image_file
        ]
        if markup_url:
            fields["markup"] = markup_url
        if markup_file:
            annotation = Path(markup_file)
            files.append(("markup", (annotation.name, annotation.read_bytes(), "image/png")))
        if mask_file:
            mask_path = Path(mask_file)
            files.append(
                ("mask", (mask_path.name, mask_path.read_bytes(), "application/octet-stream"))
            )

        try:
            result = client.image_edits_multipart(fields=fields, files=files)
            if output_json:
                print_json(result)
            else:
                print_image_result(result)
            return
        except OpenAIError as e:
            print_error(e.message)
            raise SystemExit(1) from e

    image: str | list[str] = image_url[0] if len(image_url) == 1 else list(image_url)
    payload: dict[str, object] = {
        "prompt": prompt,
        "image": image,
        "model": model,
        "n": count,
        "size": size,
        "quality": quality,
        "complexity": complexity,
        "output_format": output_format,
        "frame_count": frame_count,
        "frame_duration_ms": frame_duration_ms,
        "background": background,
        "input_fidelity": input_fidelity,
        "output_compression": output_compression,
        "response_format": response_format,
        "callback_url": callback_url,
        "async": async_mode,
    }

    if markup_url:
        payload["markup"] = markup_url
    if markup_file:
        payload["markup"] = (
            "data:image/png;base64," + base64.b64encode(Path(markup_file).read_bytes()).decode()
        )
    try:
        result = client.image_edits(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_image_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

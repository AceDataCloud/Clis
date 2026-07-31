"""QR code generation command for QRArt CLI."""

import click

from qrart_cli.core.client import get_client
from qrart_cli.core.exceptions import QRArtError
from qrart_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_TYPE,
    ECL_VALUES,
    MARKER_SHAPES,
    PADDING_LEVELS,
    PADDING_NOISE_VALUES,
    PATTERNS,
    PIXEL_STYLES,
    POSITIONS,
    PRESETS,
    QR_TYPES,
    ROTATIONS,
    SUB_MARKERS,
    print_error,
    print_json,
    print_qr_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "--type",
    "qr_type",
    type=click.Choice(QR_TYPES),
    default=DEFAULT_TYPE,
    show_default=True,
    help="QR code content type.",
)
@click.option(
    "--content",
    default=None,
    help="The QR code content (URL, text, email, phone number, etc.).",
)
@click.option(
    "--preset",
    type=click.Choice(PRESETS),
    default=None,
    help="Predefined style preset.",
)
@click.option(
    "--pattern",
    type=click.Choice(PATTERNS),
    default=None,
    help="QR code pattern style.",
)
@click.option(
    "--pixel-style",
    type=click.Choice(PIXEL_STYLES),
    default=None,
    help="Pixel shape style.",
)
@click.option(
    "--marker-shape",
    type=click.Choice(MARKER_SHAPES),
    default=None,
    help="Corner marker shape.",
)
@click.option(
    "--sub-marker",
    type=click.Choice(SUB_MARKERS),
    default=None,
    help="Inner corner marker shape.",
)
@click.option(
    "--position",
    type=click.Choice(POSITIONS),
    default=None,
    help="Logo/image position within QR code.",
)
@click.option(
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    show_default=True,
    help="Output image aspect ratio.",
)
@click.option(
    "--ecl",
    type=click.Choice(ECL_VALUES),
    default=None,
    help="Error correction level (L/M/Q/H).",
)
@click.option(
    "--rotate",
    type=click.Choice([str(r) for r in ROTATIONS]),
    default=None,
    help="QR code rotation in degrees.",
)
@click.option(
    "--padding-level",
    type=click.Choice([str(p) for p in PADDING_LEVELS]),
    default=None,
    help="Padding level around the QR code.",
)
@click.option(
    "--padding-noise",
    type=click.Choice([str(p) for p in PADDING_NOISE_VALUES]),
    default=None,
    help="Padding noise level.",
)
@click.option(
    "--qrw",
    type=float,
    default=None,
    help="QR code weight/strength.",
)
@click.option(
    "--steps",
    type=float,
    default=None,
    help="Diffusion steps.",
)
@click.option(
    "--seed",
    type=float,
    default=None,
    help="Random seed for reproducibility.",
)
@click.option(
    "--rawurl",
    is_flag=True,
    default=False,
    help="Use raw URL encoding.",
)
@click.option(
    "--content-image-url",
    default=None,
    help="URL of an image to embed in the QR code.",
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
    prompt: str,
    qr_type: str,
    content: str | None,
    preset: str | None,
    pattern: str | None,
    pixel_style: str | None,
    marker_shape: str | None,
    sub_marker: str | None,
    position: str | None,
    aspect_ratio: str,
    ecl: str | None,
    rotate: str | None,
    padding_level: str | None,
    padding_noise: str | None,
    qrw: float | None,
    steps: float | None,
    seed: float | None,
    rawurl: bool,
    content_image_url: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate an art QR code from a text prompt.

    PROMPT is the artistic style description for the QR code background.

    \b
    Examples:
      qrart generate "A beautiful sunset over the ocean" --content https://example.com
      qrart generate "Futuristic city" --type link --content https://example.com \\
            --preset neon-mech
      qrart generate "Cherry blossoms" --content https://example.com \\
            --pattern s1 --pixel-style rounded
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "prompt": prompt,
        "type": qr_type,
        "aspect_ratio": aspect_ratio,
    }
    if content:
        payload["content"] = content
    if preset:
        payload["preset"] = preset
    if pattern:
        payload["pattern"] = pattern
    if pixel_style:
        payload["pixel_style"] = pixel_style
    if marker_shape:
        payload["marker_shape"] = marker_shape
    if sub_marker:
        payload["sub_marker"] = sub_marker
    if position:
        payload["position"] = position
    if ecl:
        payload["ecl"] = ecl
    if rotate is not None:
        payload["rotate"] = int(rotate)
    if padding_level is not None:
        payload["padding_level"] = int(padding_level)
    if padding_noise is not None:
        payload["padding_noise"] = float(padding_noise)
    if qrw is not None:
        payload["qrw"] = qrw
    if steps is not None:
        payload["steps"] = steps
    if seed is not None:
        payload["seed"] = seed
    if rawurl:
        payload["rawurl"] = True
    if content_image_url:
        payload["content_image_url"] = content_image_url
    if callback_url:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate(**payload)
        if output_json:
            print_json(result)
        else:
            print_qr_result(result)
    except QRArtError as e:
        print_error(e.message)
        raise SystemExit(1) from e

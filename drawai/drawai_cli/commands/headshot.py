"""Headshot generation command for DrawAI CLI."""

import click

from drawai_cli.core.client import get_client
from drawai_cli.core.exceptions import DrawAIError
from drawai_cli.core.output import (
    DEFAULT_MODE,
    DEFAULT_TEMPLATE,
    MODES,
    TEMPLATES,
    print_error,
    print_headshot_result,
    print_json,
)


@click.command()
@click.option(
    "--image-url",
    "image_urls",
    multiple=True,
    required=True,
    help="URL(s) of the face image(s) to use. Can be specified multiple times.",
)
@click.option(
    "--template",
    type=click.Choice(TEMPLATES),
    default=DEFAULT_TEMPLATE,
    show_default=True,
    help="Photo template/style to apply.",
)
@click.option(
    "--mode",
    type=click.Choice(MODES),
    default=DEFAULT_MODE,
    show_default=True,
    help="Generation mode: fast or relax (higher quality).",
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
    image_urls: tuple[str, ...],
    template: str,
    mode: str,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate an AI headshot or ID photo.

    Provide one or more face image URLs with --image-url.

    \b
    Examples:
      drawai generate --image-url https://example.com/face.jpg
      drawai generate --image-url https://example.com/face.jpg --template wedding
      drawai generate --image-url https://example.com/face.jpg --mode relax --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "mode": mode,
        "template": template,
        "image_urls": list(image_urls),
    }
    if callback_url:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate_headshot(**payload)
        if output_json:
            print_json(result)
        else:
            print_headshot_result(result)
    except DrawAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

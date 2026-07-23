"""Image2Text recognition command."""

import click

from image2text_cli.core.client import get_client
from image2text_cli.core.exceptions import Image2TextError
from image2text_cli.core.output import (
    print_error,
    print_json,
    print_recognition_result,
)


@click.command()
@click.argument("image")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Return immediately with a task_id instead of blocking until the captcha is solved.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def recognize(
    ctx: click.Context,
    image: str,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Recognize text from a captcha image.

    IMAGE is the base64-encoded image data or a URL to the captcha image.

    \\b
    Examples:
      image2text recognize /9j/4AAQSkZJRgAB...
      image2text recognize /9j/4AAQSkZJRgAB... --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {"image": image}
    if async_mode:
        payload["async"] = True

    try:
        result = client.recognize(**payload)
        if output_json:
            print_json(result)
        else:
            print_recognition_result(result)
    except Image2TextError as e:
        print_error(e.message)
        raise SystemExit(1) from e

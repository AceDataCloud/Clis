"""Describe, shorten, translate, and seed utility commands."""

import click

from midjourney_cli.core.client import get_client
from midjourney_cli.core.exceptions import MidjourneyError
from midjourney_cli.core.output import print_error, print_json, print_result


@click.command()
@click.option("--image-url", required=True, help="URL of the image to describe.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def describe(
    ctx: click.Context,
    image_url: str,
    output_json: bool,
) -> None:
    """Describe an image with Midjourney.

    Examples:

      midjourney describe --image-url https://example.com/photo.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.describe(image_url=image_url)
        if output_json:
            print_json(result)
        else:
            print_result(result, title="Describe Result")
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def shorten(
    ctx: click.Context,
    prompt: str,
    output_json: bool,
) -> None:
    """Shorten a Midjourney prompt.

    PROMPT is the long prompt to shorten.

    Examples:

      midjourney shorten "A very long and detailed prompt that needs to be shortened"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.shorten(prompt=prompt)
        if output_json:
            print_json(result)
        else:
            print_result(result, title="Shorten Result")
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("content")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def translate(
    ctx: click.Context,
    content: str,
    output_json: bool,
) -> None:
    """Translate content for Midjourney.

    CONTENT is the text to translate.

    Examples:

      midjourney translate "Una hermosa puesta de sol sobre el oceano"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.translate(content=content)
        if output_json:
            print_json(result)
        else:
            print_result(result, title="Translate Result")
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.option("--image-id", required=True, help="Image ID to retrieve the seed for.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def seed(
    ctx: click.Context,
    image_id: str,
    output_json: bool,
) -> None:
    """Retrieve the seed for a generated image.

    Examples:

      midjourney seed --image-id abc123
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.seed(image_id=image_id)
        if output_json:
            print_json(result)
        else:
            print_result(result, title="Seed Result")
    except MidjourneyError as e:
        print_error(e.message)
        raise SystemExit(1) from e

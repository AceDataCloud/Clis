"""QwenImage generation commands."""

from collections.abc import Callable
from typing import Any

import click

from qwen_image_cli.core.client import get_client
from qwen_image_cli.core.exceptions import QwenImageError
from qwen_image_cli.core.output import (
    DEFAULT_MODEL,
    MODELS,
    print_error,
    print_image_result,
    print_json,
)


def common(fn: Callable[..., Any]) -> Callable[..., Any]:
    for decorator in reversed(
        [
            click.option("--model", type=click.Choice(MODELS), default=DEFAULT_MODEL),
            click.option("--size", default=None, help="WIDTH*HEIGHT"),
            click.option("-n", type=click.IntRange(1, 6), default=1),
            click.option("--prompt-extend/--no-prompt-extend", default=True),
            click.option("--enable-thinking/--no-enable-thinking", default=True),
            click.option("--negative-prompt", default=None),
            click.option("--seed", type=click.IntRange(0, 2147483647), default=None),
            click.option("--watermark/--no-watermark", default=False),
            click.option("--callback-url", default=None),
            click.option("--async", "async_mode", is_flag=True),
            click.option("--json", "output_json", is_flag=True),
        ]
    ):
        fn = decorator(fn)
    return fn


def run(ctx: click.Context, prompt: str, image_urls: list[str] | None, **kwargs: Any) -> None:
    output_json = kwargs.pop("output_json")
    async_mode = kwargs.pop("async_mode")
    payload = {"prompt": prompt, "image_urls": image_urls or None, **kwargs, "async": async_mode}
    try:
        result = get_client(ctx.obj.get("token")).generate_image(**payload)
        (print_json if output_json else print_image_result)(result)
    except QwenImageError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("prompt")
@common
@click.pass_context
def generate(ctx: click.Context, prompt: str, **kwargs: Any) -> None:
    """Generate images from PROMPT."""
    run(ctx, prompt, None, **kwargs)


@click.command()
@click.argument("prompt")
@click.option("-i", "--image-url", "image_urls", multiple=True, required=True)
@common
@click.pass_context
def edit(ctx: click.Context, prompt: str, image_urls: tuple[str, ...], **kwargs: Any) -> None:
    """Edit one to three reference images."""
    if len(image_urls) > 3:
        raise click.BadParameter("at most 3 image URLs")
    run(ctx, prompt, list(image_urls), **kwargs)

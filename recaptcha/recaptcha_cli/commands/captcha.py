"""reCAPTCHA recognition and token commands."""

import click

from recaptcha_cli.core.client import get_client
from recaptcha_cli.core.exceptions import RecaptchaError
from recaptcha_cli.core.output import (
    print_error,
    print_json,
    print_recognition_result,
    print_token_result,
)


@click.command()
@click.argument("image")
@click.argument("question")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Return immediately with a task_id instead of blocking until recognized.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def recognize2(
    ctx: click.Context,
    image: str,
    question: str,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Recognize a reCAPTCHA v2 challenge.

    IMAGE is the URL or base64-encoded content of the captcha image.
    QUESTION is the challenge question (e.g. "Select all cars").

    \\b
    Examples:
      recaptcha recognize2 https://example.com/captcha.jpg "Select all cars"
      recaptcha recognize2 https://example.com/captcha.jpg "Select all buses" --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "image": image,
        "question": question,
    }
    if async_mode:
        payload["async"] = True

    try:
        result = client.recognize2(**payload)
        if output_json:
            print_json(result)
        else:
            print_recognition_result(result)
    except RecaptchaError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("website_key")
@click.argument("website_url")
@click.option(
    "--proxy",
    default=None,
    help="Optional proxy URL to use while solving the captcha.",
)
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Return immediately with a task_id instead of blocking until the token is solved.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def token2(
    ctx: click.Context,
    website_key: str,
    website_url: str,
    proxy: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Solve reCAPTCHA v2 and retrieve a token.

    WEBSITE_KEY is the reCAPTCHA site key for the target website.
    WEBSITE_URL is the URL of the page where the captcha appears.

    \\b
    Examples:
      recaptcha token2 6LcXxxxxxxxxxxxxxx https://example.com
      recaptcha token2 6LcXxxxxxxxxxxxxxx https://example.com --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "website_key": website_key,
        "website_url": website_url,
    }
    if proxy is not None:
        payload["proxy"] = proxy
    if async_mode:
        payload["async"] = True

    try:
        result = client.token2(**payload)
        if output_json:
            print_json(result)
        else:
            print_token_result(result)
    except RecaptchaError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("website_key")
@click.argument("website_url")
@click.option(
    "--page-action",
    required=True,
    help="The action name associated with the protected element (e.g. 'submit', 'login').",
)
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Return immediately with a task_id instead of blocking until the token is solved.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def token3(
    ctx: click.Context,
    website_key: str,
    website_url: str,
    page_action: str,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Solve reCAPTCHA v3 and retrieve a token.

    WEBSITE_KEY is the reCAPTCHA v3 site key for the target website.
    WEBSITE_URL is the URL of the page where the captcha appears.

    \\b
    Examples:
      recaptcha token3 6LcXxxxxxxxxxxxxxx https://example.com --page-action submit
      recaptcha token3 6LcXxxxxxxxxxxxxxx https://example.com --page-action login --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "website_key": website_key,
        "website_url": website_url,
        "page_action": page_action,
    }
    if async_mode:
        payload["async"] = True

    try:
        result = client.token3(**payload)
        if output_json:
            print_json(result)
        else:
            print_token_result(result)
    except RecaptchaError as e:
        print_error(e.message)
        raise SystemExit(1) from e

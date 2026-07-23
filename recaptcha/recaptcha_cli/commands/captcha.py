"""Recaptcha recognition and token commands."""

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
    help="Return immediately with a task_id instead of blocking until the captcha is solved.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def recognize(
    ctx: click.Context,
    image: str,
    question: str,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Recognize reCAPTCHA v2 challenge images.

    IMAGE is the base64-encoded image data for the captcha.
    QUESTION is the question or instruction for the recognition task.

    \\b
    Examples:
      recaptcha recognize /9j/4AAQSkZJRgAB... "/m/0k4j"
      recaptcha recognize /9j/4AAQSkZJRgAB... "/m/0k4j" --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "image": image,
        "question": question,
    }
    if async_mode:
        payload["async"] = True

    try:
        result = client.recognize(**payload)
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
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Return immediately with a task_id instead of blocking until the token is solved.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def token(
    ctx: click.Context,
    website_key: str,
    website_url: str,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Solve reCAPTCHA v2 and retrieve a token.

    WEBSITE_KEY is the reCAPTCHA v2 site key for the target website.
    WEBSITE_URL is the URL of the page where the captcha appears.

    \\b
    Examples:
      recaptcha token 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com
      recaptcha token 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "website_key": website_key,
        "website_url": website_url,
    }
    if async_mode:
        payload["async"] = True

    try:
        result = client.get_token2(**payload)
        if output_json:
            print_json(result)
        else:
            print_token_result(result, title="reCAPTCHA v2 Token Result")
    except RecaptchaError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("website_key")
@click.argument("website_url")
@click.argument("page_action")
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
    PAGE_ACTION is the action name for reCAPTCHA v3 verification.

    \\b
    Examples:
      recaptcha token3 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com login
      recaptcha token3 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com login --async
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
        result = client.get_token3(**payload)
        if output_json:
            print_json(result)
        else:
            print_token_result(result, title="reCAPTCHA v3 Token Result")
    except RecaptchaError as e:
        print_error(e.message)
        raise SystemExit(1) from e

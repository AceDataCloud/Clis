"""hCaptcha recognition and token commands."""

import json

import click

from hcaptcha_cli.core.client import get_client
from hcaptcha_cli.core.exceptions import HcaptchaError
from hcaptcha_cli.core.output import (
    print_error,
    print_json,
    print_recognition_result,
    print_token_result,
)


def _parse_json_array_option(value: str | None, option_name: str) -> list[object] | None:
    """Parse a JSON array option."""
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be valid JSON.") from exc
    if not isinstance(parsed, list):
        raise click.BadParameter(f"{option_name} must be a JSON array.")
    return parsed


@click.command()
@click.option(
    "--queries",
    default=None,
    help="Image URLs to classify as a JSON array.",
)
@click.option(
    "--question",
    default=None,
    help="Question or instruction for the recognition task.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def recognize(
    ctx: click.Context,
    queries: str | None,
    question: str | None,
    output_json: bool,
) -> None:
    """Recognize hCaptcha challenge images.

    \\b
    Examples:
      hcaptcha recognize --queries '["https://example.com/img1.jpg"]' --question "Select all cars"
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {}
    parsed_queries = _parse_json_array_option(queries, "--queries")
    if parsed_queries is not None:
        payload["queries"] = parsed_queries
    if question is not None:
        payload["question"] = question

    try:
        result = client.recognize(**payload)
        if output_json:
            print_json(result)
        else:
            print_recognition_result(result)
    except HcaptchaError as e:
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
    """Solve hCaptcha and retrieve a token.

    WEBSITE_KEY is the hCaptcha site key for the target website.
    WEBSITE_URL is the URL of the page where the captcha appears.

    \\b
    Examples:
      hcaptcha token a5f74b19-9e45-40e0-b45d-47ff91b7a6c2 https://accounts.hcaptcha.com/demo
      hcaptcha token a5f74b19-9e45-40e0-b45d-47ff91b7a6c2 https://example.com --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "website_key": website_key,
        "website_url": website_url,
    }
    if async_mode:
        payload["async"] = True

    try:
        result = client.get_token(**payload)
        if output_json:
            print_json(result)
        else:
            print_token_result(result)
    except HcaptchaError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""hCaptcha recognition and token commands."""

import json

import click

from hcaptcha_cli.core.client import get_client
from hcaptcha_cli.core.exceptions import HcaptchaAPIError, HcaptchaError
from hcaptcha_cli.core.output import (
    print_error,
    print_json,
    print_recognition_result,
    print_task_result,
    print_token_result,
)


def _parse_json_array_option(value: str | None, option_name: str) -> list[str] | None:
    """Parse a JSON array option."""
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be valid JSON.") from exc
    if not isinstance(parsed, list):
        raise click.BadParameter(f"{option_name} must be a JSON array.")
    if not all(isinstance(item, str) for item in parsed):
        raise click.BadParameter(f"{option_name} must be a JSON array of strings.")
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
    queries: str | None,
    question: str | None,
    async_mode: bool,
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
    if async_mode:
        payload["async"] = True

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
@click.option(
    "--proxy",
    default=None,
    help="Optional proxy URL to use while solving the captcha.",
)
@click.option(
    "--rqdata",
    default=None,
    help="Optional hCaptcha rqdata value for the captcha challenge.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def token(
    ctx: click.Context,
    website_key: str,
    website_url: str,
    async_mode: bool,
    proxy: str | None,
    rqdata: str | None,
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
    if proxy is not None:
        payload["proxy"] = proxy
    if rqdata is not None:
        payload["rqdata"] = rqdata
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


@click.command()
@click.argument("task_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def task(
    ctx: click.Context,
    task_id: str,
    output_json: bool,
) -> None:
    """Read the persisted status of an asynchronous captcha task.

    TASK_ID is the task identifier returned when calling recognize or token with --async.

    \\b
    Examples:
      hcaptcha task 61138bb6-19aa-11ec-a9c8-0242ac110002
      hcaptcha task 61138bb6-19aa-11ec-a9c8-0242ac110002 --json
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {"task_id": task_id}

    try:
        result = client.get_task(**payload)
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except HcaptchaError as e:
        if output_json and isinstance(e, HcaptchaAPIError) and e.status_code == 504:
            try:
                print_json(json.loads(e.message))
            except json.JSONDecodeError:
                print_error(e.message)
        else:
            print_error(e.message)
        raise SystemExit(1) from e

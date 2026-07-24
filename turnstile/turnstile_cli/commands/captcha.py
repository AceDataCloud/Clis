"""Turnstile token command."""

import click

from turnstile_cli.core.client import get_client
from turnstile_cli.core.exceptions import TurnstileError
from turnstile_cli.core.output import (
    print_error,
    print_json,
    print_token_result,
)


@click.command()
@click.argument("website_key")
@click.argument("website_url")
@click.option(
    "--action",
    default=None,
    help="Turnstile action identifier for the target website.",
)
@click.option(
    "--cdata",
    default=None,
    help="Turnstile cdata for the target website.",
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
def token(
    ctx: click.Context,
    website_key: str,
    website_url: str,
    action: str | None,
    cdata: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Solve Cloudflare Turnstile and retrieve a token.

    WEBSITE_KEY is the Turnstile site key for the target website.
    WEBSITE_URL is the URL of the page where the captcha appears.

    \\b
    Examples:
      turnstile token 0x4AAAAAAADnPIDROrmt1Wwj https://react-turnstile.vercel.app
      turnstile token 0x4AAAAAAADnPIDROrmt1Wwj https://example.com --action login
      turnstile token 0x4AAAAAAADnPIDROrmt1Wwj https://example.com --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "website_key": website_key,
        "website_url": website_url,
    }
    if action is not None:
        payload["action"] = action
    if cdata is not None:
        payload["cdata"] = cdata
    if async_mode:
        payload["async"] = True

    try:
        result = client.get_token(**payload)
        if output_json:
            print_json(result)
        else:
            print_token_result(result)
    except TurnstileError as e:
        print_error(e.message)
        raise SystemExit(1) from e

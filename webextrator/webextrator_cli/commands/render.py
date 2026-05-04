"""Web page render command."""

import click

from webextrator_cli.core.client import get_client
from webextrator_cli.core.exceptions import WebExtraterError
from webextrator_cli.core.output import (
    BLOCK_RESOURCE_TYPES,
    WAIT_UNTIL_OPTIONS,
    print_error,
    print_json,
    print_render_result,
)


@click.command()
@click.argument("url")
@click.option(
    "--wait-until",
    type=click.Choice(WAIT_UNTIL_OPTIONS),
    default=None,
    help="Page load wait condition (default: networkidle).",
)
@click.option(
    "--timeout",
    type=float,
    default=None,
    help="Total timeout in seconds for the render operation (default: 30).",
)
@click.option(
    "--delay",
    type=float,
    default=None,
    help="Extra delay in seconds after page load, before HTML is captured.",
)
@click.option(
    "--wait-for-selector",
    default=None,
    help="CSS selector to wait for before capturing HTML.",
)
@click.option(
    "--block-resource",
    "block_resources",
    type=click.Choice(BLOCK_RESOURCE_TYPES),
    multiple=True,
    help="Resource types to block during page load (repeatable).",
)
@click.option(
    "--user-agent",
    default=None,
    help="Override the User-Agent header.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Webhook callback URL for async processing.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def render(
    ctx: click.Context,
    url: str,
    wait_until: str | None,
    timeout: float | None,
    delay: float | None,
    wait_for_selector: str | None,
    block_resources: tuple[str, ...],
    user_agent: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Render a web page and return the rendered HTML.

    URL is the web page to render.

    \b
    Examples:
      webextrator render https://example.com
      webextrator render https://example.com --wait-until load --json
      webextrator render https://example.com --block-resource image --block-resource font
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "url": url,
        "wait_until": wait_until,
        "timeout": timeout,
        "delay": delay,
        "wait_for_selector": wait_for_selector,
        "block_resources": list(block_resources) if block_resources else None,
        "user_agent": user_agent,
        "callback_url": callback_url,
    }

    try:
        result = client.render(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_render_result(result)
    except WebExtraterError as e:
        print_error(e.message)
        raise SystemExit(1) from e

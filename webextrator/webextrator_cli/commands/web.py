"""Web extraction and rendering commands."""

import click

from webextrator_cli.core.client import get_client
from webextrator_cli.core.exceptions import WebExtraterError
from webextrator_cli.core.output import (
    WAIT_UNTIL_OPTIONS,
    print_error,
    print_extract_result,
    print_json,
    print_render_result,
)


@click.command()
@click.argument("url")
@click.option(
    "--expected-type",
    type=click.Choice(["product", "article", "general"]),
    default=None,
    help="Hint about the expected page type to optimize extraction.",
)
@click.option(
    "--enable-llm",
    is_flag=True,
    default=False,
    help="Enable LLM-based semantic normalization as a final extraction step.",
)
@click.option(
    "--wait-until",
    type=click.Choice(WAIT_UNTIL_OPTIONS),
    default=None,
    help="Page load wait condition (default: networkidle).",
)
@click.option(
    "--timeout",
    default=None,
    type=float,
    help="Total timeout in seconds for the extract operation (default: 30).",
)
@click.option(
    "--delay",
    default=None,
    type=float,
    help="Extra delay in seconds after the page is loaded, before extraction.",
)
@click.option(
    "--wait-for-selector",
    default=None,
    help="CSS selector to wait for before starting extraction.",
)
@click.option(
    "--user-agent",
    default=None,
    help="Override the User-Agent header.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Callback URL for async processing.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def extract(
    ctx: click.Context,
    url: str,
    expected_type: str | None,
    enable_llm: bool,
    wait_until: str | None,
    timeout: float | None,
    delay: float | None,
    wait_for_selector: str | None,
    user_agent: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Extract structured content from a web page.

    URL is the address of the web page to extract content from.

    \b
    Examples:
      webextrator extract https://www.amazon.com/dp/B0C1234567
      webextrator extract https://example.com/article --expected-type article
      webextrator extract https://shop.example.com --enable-llm
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "url": url,
        "expected_type": expected_type,
        "enable_llm": enable_llm if enable_llm else None,
        "wait_until": wait_until,
        "timeout": timeout,
        "delay": delay,
        "wait_for_selector": wait_for_selector,
        "user_agent": user_agent,
        "callback_url": callback_url,
    }

    try:
        result = client.extract(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_extract_result(result)
    except WebExtraterError as e:
        print_error(e.message)
        raise SystemExit(1) from e


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
    default=None,
    type=float,
    help="Total timeout in seconds for the render operation (default: 30).",
)
@click.option(
    "--delay",
    default=None,
    type=float,
    help="Extra delay in seconds after the page is loaded, before HTML is captured.",
)
@click.option(
    "--wait-for-selector",
    default=None,
    help="CSS selector to wait for before capturing HTML.",
)
@click.option(
    "--user-agent",
    default=None,
    help="Override the User-Agent header.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Callback URL for async processing.",
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
    user_agent: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Render a web page and return the rendered HTML.

    URL is the address of the web page to render.

    \b
    Examples:
      webextrator render https://example.com
      webextrator render https://example.com --wait-until load
      webextrator render https://spa.example.com --delay 2 --wait-for-selector "#app"
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "url": url,
        "wait_until": wait_until,
        "timeout": timeout,
        "delay": delay,
        "wait_for_selector": wait_for_selector,
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

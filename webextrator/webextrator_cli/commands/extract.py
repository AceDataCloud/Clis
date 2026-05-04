"""Web page extract command."""

import click

from webextrator_cli.core.client import get_client
from webextrator_cli.core.exceptions import WebExtraterError
from webextrator_cli.core.output import (
    BLOCK_RESOURCE_TYPES,
    EXPECTED_TYPES,
    WAIT_UNTIL_OPTIONS,
    print_error,
    print_extract_result,
    print_json,
)


@click.command()
@click.argument("url")
@click.option(
    "--expected-type",
    type=click.Choice(EXPECTED_TYPES),
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
    type=float,
    default=None,
    help="Total timeout in seconds for the extract operation (default: 30).",
)
@click.option(
    "--delay",
    type=float,
    default=None,
    help="Extra delay in seconds after page load, before extraction.",
)
@click.option(
    "--wait-for-selector",
    default=None,
    help="CSS selector to wait for before starting extraction.",
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
def extract(
    ctx: click.Context,
    url: str,
    expected_type: str | None,
    enable_llm: bool,
    wait_until: str | None,
    timeout: float | None,
    delay: float | None,
    wait_for_selector: str | None,
    block_resources: tuple[str, ...],
    user_agent: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Extract structured content from a web page.

    URL is the web page to extract content from.

    \b
    Examples:
      webextrator extract https://www.amazon.com/dp/B0C1234567
      webextrator extract https://example.com/article --expected-type article
      webextrator extract https://example.com --enable-llm --json
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
        "block_resources": list(block_resources) if block_resources else None,
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

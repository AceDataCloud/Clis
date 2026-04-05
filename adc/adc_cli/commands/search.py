"""Search commands."""

import click

from adc_cli.core.client import get_client
from adc_cli.core.exceptions import AdcError
from adc_cli.core.output import print_error, print_json, print_search_result


@click.command()
@click.argument("query")
@click.option(
    "-t",
    "--type",
    "search_type",
    type=click.Choice(["search", "images", "news", "maps", "places", "videos"]),
    default="search",
    help="Type of search.",
)
@click.option("-c", "--country", default=None, help="Country code (e.g. us, cn, uk).")
@click.option("-l", "--language", default=None, help="Language code (e.g. en, zh-cn).")
@click.option("--time-range", default=None, help="Time filter: qdr:h, qdr:d, qdr:w, qdr:m.")
@click.option("-n", "--number", default=None, type=int, help="Number of results.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def search(
    ctx: click.Context,
    query: str,
    search_type: str,
    country: str | None,
    language: str | None,
    time_range: str | None,
    number: int | None,
    output_json: bool,
) -> None:
    """Search Google using SERP API.

    QUERY is the search query.

    \b
    Examples:
      adc search "artificial intelligence"
      adc search "tech news" -t news --time-range qdr:d
      adc search "sunset photos" -t images -c us
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "query": query,
            "type": search_type,
            "country": country,
            "language": language,
            "range": time_range,
            "number": number,
        }

        result = client.serp_search(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_search_result(result)
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e

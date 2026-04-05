"""Search commands."""

import click

from serp_cli.core.client import get_client
from serp_cli.core.exceptions import SerpError
from serp_cli.core.output import (
    SEARCH_TYPES,
    print_error,
    print_json,
    print_search_result,
)


@click.command()
@click.argument("query")
@click.option(
    "-t",
    "--type",
    "search_type",
    type=click.Choice(SEARCH_TYPES),
    default="search",
    help="Type of search to perform.",
)
@click.option(
    "-c",
    "--country",
    default=None,
    help="Country code for localized results (e.g. us, cn, uk).",
)
@click.option(
    "-l",
    "--language",
    default=None,
    help="Language code for results (e.g. en, zh-cn, fr).",
)
@click.option(
    "--time-range",
    default=None,
    help="Time filter: qdr:h (hour), qdr:d (day), qdr:w (week), qdr:m (month).",
)
@click.option(
    "-n",
    "--number",
    default=None,
    type=int,
    help="Number of results per page (default: 10).",
)
@click.option(
    "-p",
    "--page",
    default=None,
    type=int,
    help="Page number for pagination.",
)
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
    page: int | None,
    output_json: bool,
) -> None:
    """Search Google and get structured results.

    QUERY is the search query string.

    \b
    Examples:
      serp search "artificial intelligence"
      serp search "tech news" -t news --time-range qdr:d
      serp search "best restaurants" -t places -c uk
      serp search "sunset photography" -t images -n 20
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
            "page": page,
        }

        result = client.search(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_search_result(result)
    except SerpError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("query")
@click.option("-c", "--country", default=None, help="Country code (e.g. us, cn, uk).")
@click.option("-l", "--language", default=None, help="Language code (e.g. en, zh-cn).")
@click.option("-n", "--number", default=None, type=int, help="Number of results.")
@click.option("-p", "--page", default=None, type=int, help="Page number.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def images(
    ctx: click.Context,
    query: str,
    country: str | None,
    language: str | None,
    number: int | None,
    page: int | None,
    output_json: bool,
) -> None:
    """Search Google Images.

    QUERY is the image search query.

    Examples:

      serp images "sunset photography"
    """
    ctx.invoke(
        search,
        query=query,
        search_type="images",
        country=country,
        language=language,
        time_range=None,
        number=number,
        page=page,
        output_json=output_json,
    )


@click.command()
@click.argument("query")
@click.option("-c", "--country", default=None, help="Country code (e.g. us, cn, uk).")
@click.option("-l", "--language", default=None, help="Language code (e.g. en, zh-cn).")
@click.option(
    "--time-range",
    default=None,
    help="Time filter: qdr:h, qdr:d, qdr:w, qdr:m.",
)
@click.option("-n", "--number", default=None, type=int, help="Number of results.")
@click.option("-p", "--page", default=None, type=int, help="Page number.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def news(
    ctx: click.Context,
    query: str,
    country: str | None,
    language: str | None,
    time_range: str | None,
    number: int | None,
    page: int | None,
    output_json: bool,
) -> None:
    """Search Google News.

    QUERY is the news search query.

    Examples:

      serp news "AI breakthrough" --time-range qdr:d
    """
    ctx.invoke(
        search,
        query=query,
        search_type="news",
        country=country,
        language=language,
        time_range=time_range,
        number=number,
        page=page,
        output_json=output_json,
    )


@click.command()
@click.argument("query")
@click.option("-c", "--country", default=None, help="Country code (e.g. us, cn, uk).")
@click.option("-l", "--language", default=None, help="Language code (e.g. en, zh-cn).")
@click.option("-n", "--number", default=None, type=int, help="Number of results.")
@click.option("-p", "--page", default=None, type=int, help="Page number.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def videos(
    ctx: click.Context,
    query: str,
    country: str | None,
    language: str | None,
    number: int | None,
    page: int | None,
    output_json: bool,
) -> None:
    """Search Google Videos.

    QUERY is the video search query.

    Examples:

      serp videos "how to cook pasta"
    """
    ctx.invoke(
        search,
        query=query,
        search_type="videos",
        country=country,
        language=language,
        time_range=None,
        number=number,
        page=page,
        output_json=output_json,
    )


@click.command()
@click.argument("query")
@click.option("-c", "--country", default=None, help="Country code (e.g. us, cn, uk).")
@click.option("-l", "--language", default=None, help="Language code (e.g. en, zh-cn).")
@click.option("-n", "--number", default=None, type=int, help="Number of results.")
@click.option("-p", "--page", default=None, type=int, help="Page number.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def places(
    ctx: click.Context,
    query: str,
    country: str | None,
    language: str | None,
    number: int | None,
    page: int | None,
    output_json: bool,
) -> None:
    """Search Google for local places and businesses.

    QUERY is the places search query.

    Examples:

      serp places "coffee shops near Times Square"
    """
    ctx.invoke(
        search,
        query=query,
        search_type="places",
        country=country,
        language=language,
        time_range=None,
        number=number,
        page=page,
        output_json=output_json,
    )


@click.command()
@click.argument("query")
@click.option("-c", "--country", default=None, help="Country code (e.g. us, cn, uk).")
@click.option("-l", "--language", default=None, help="Language code (e.g. en, zh-cn).")
@click.option("-n", "--number", default=None, type=int, help="Number of results.")
@click.option("-p", "--page", default=None, type=int, help="Page number.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def maps(
    ctx: click.Context,
    query: str,
    country: str | None,
    language: str | None,
    number: int | None,
    page: int | None,
    output_json: bool,
) -> None:
    """Search Google Maps for locations.

    QUERY is the maps search query.

    Examples:

      serp maps "Eiffel Tower"
    """
    ctx.invoke(
        search,
        query=query,
        search_type="maps",
        country=country,
        language=language,
        time_range=None,
        number=number,
        page=page,
        output_json=output_json,
    )

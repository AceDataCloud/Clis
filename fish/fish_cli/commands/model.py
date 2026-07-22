"""Model query commands."""

import click

from fish_cli.core.client import get_client
from fish_cli.core.exceptions import FishError
from fish_cli.core.output import print_error, print_json, print_model_detail, print_model_list


@click.command("models")
@click.option(
    "--page-size",
    type=int,
    default=10,
    show_default=True,
    help="Number of models per page.",
)
@click.option(
    "--page-number",
    type=int,
    default=1,
    show_default=True,
    help="Page number (starting from 1).",
)
@click.option(
    "--title",
    default=None,
    help="Fuzzy search by model title.",
)
@click.option(
    "--tag",
    default=None,
    help="Filter by tag.",
)
@click.option(
    "--self",
    "self_only",
    is_flag=True,
    default=False,
    help="Only return voice models created by the current account.",
)
@click.option(
    "--author-id",
    default=None,
    help="Filter by creator ID.",
)
@click.option(
    "--language",
    default=None,
    help="Filter by voice model language.",
)
@click.option(
    "--title-language",
    default=None,
    help="Filter by title language.",
)
@click.option(
    "--sort-by",
    default=None,
    help="Sort models by a specific field.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def models(
    ctx: click.Context,
    page_size: int,
    page_number: int,
    title: str | None,
    tag: str | None,
    self_only: bool,
    author_id: str | None,
    language: str | None,
    title_language: str | None,
    sort_by: str | None,
    output_json: bool,
) -> None:
    """List available Fish voice models.

    \\b
    Examples:
      fish models
      fish models --self
      fish models --title "my voice" --language en
    """
    client = get_client(ctx.obj.get("token"))

    params: dict[str, object] = {
        "page_size": page_size,
        "page_number": page_number,
    }
    if title is not None:
        params["title"] = title
    if tag is not None:
        params["tag"] = tag
    if self_only:
        params["self"] = True
    if author_id is not None:
        params["author_id"] = author_id
    if language is not None:
        params["language"] = language
    if title_language is not None:
        params["title_language"] = title_language
    if sort_by is not None:
        params["sort_by"] = sort_by

    try:
        result = client.list_models(params=params)
        if output_json:
            print_json(result)
        else:
            print_model_list(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("model")
@click.argument("model_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def model(
    ctx: click.Context,
    model_id: str,
    output_json: bool,
) -> None:
    """Get details of a specific Fish voice model.

    MODEL_ID is the unique identifier of the voice model.

    \\b
    Examples:
      fish model d7900c21663f485ab63ebdb7e5905036
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_model(model_id)
        if output_json:
            print_json(result)
        else:
            print_model_detail(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e

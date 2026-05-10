"""Voice model commands."""

import click

from fish_cli.core.client import get_client
from fish_cli.core.exceptions import FishError
from fish_cli.core.output import print_error, print_json, print_voice_detail, print_voice_list


@click.command("voices")
@click.option(
    "--page-size",
    type=int,
    default=10,
    show_default=True,
    help="Number of items per page.",
)
@click.option(
    "--page-number",
    type=int,
    default=1,
    show_default=True,
    help="1-based page number.",
)
@click.option("--title", default=None, help="Filter by partial title match.")
@click.option("--tag", default=None, help="Filter by a single tag.")
@click.option(
    "--self",
    "only_self",
    is_flag=True,
    default=False,
    help="Only return models owned by the calling account.",
)
@click.option("--author-id", default=None, help="Filter by author ID.")
@click.option("--language", default=None, help="Filter by language code (e.g. en, zh).")
@click.option("--title-language", default=None, help="Filter by title language.")
@click.option(
    "--sort-by",
    default=None,
    help="Sort by field (e.g. created_at, task_count).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def voices(
    ctx: click.Context,
    page_size: int,
    page_number: int,
    title: str | None,
    tag: str | None,
    only_self: bool,
    author_id: str | None,
    language: str | None,
    title_language: str | None,
    sort_by: str | None,
    output_json: bool,
) -> None:
    """List available Fish AI voice models.

    Examples:

      fish voices

      fish voices --language en --page-size 20

      fish voices --tag "podcast" --json
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.list_voices(
            page_size=page_size,
            page_number=page_number,
            title=title,
            tag=tag,
            **{"self": only_self} if only_self else {},
            author_id=author_id,
            language=language,
            title_language=title_language,
            sort_by=sort_by,
        )
        if output_json:
            print_json(result)
        else:
            print_voice_list(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("voice")
@click.argument("voice_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def voice(
    ctx: click.Context,
    voice_id: str,
    output_json: bool,
) -> None:
    """Get details of a specific voice model.

    VOICE_ID is the unique identifier of the voice model.

    Examples:

      fish voice abc123def456

      fish voice abc123def456 --json
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_voice(voice_id)
        if output_json:
            print_json(result)
        else:
            print_voice_detail(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e

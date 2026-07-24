"""Lyrics generation commands."""

import click

from producer_cli.core.client import get_client
from producer_cli.core.exceptions import ProducerError
from producer_cli.core.output import print_error, print_json, print_lyrics_result


@click.command()
@click.argument("prompt")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def lyrics(
    ctx: click.Context,
    prompt: str,
    output_json: bool,
) -> None:
    """Generate song lyrics from a prompt.

    PROMPT is a description of the lyrics to generate.

    \b
    Examples:
      producer lyrics "A love song about the ocean at sunset"
      producer lyrics "Funny rap about programming bugs"
      producer lyrics "Epic ballad about adventure and discovery"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_lyrics(prompt=prompt)
        if output_json:
            print_json(result)
        else:
            print_lyrics_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e

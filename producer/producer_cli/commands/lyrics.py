"""Lyrics generation commands."""

import json

import click

from producer_cli.core.client import get_client
from producer_cli.core.exceptions import ProducerError
from producer_cli.core.output import print_error, print_json, print_lyrics_result


def _parse_prompt(prompt: str) -> str | dict[str, object]:
    """Parse JSON object prompts while preserving plain-text prompt compatibility."""
    if not prompt.lstrip().startswith("{"):
        return prompt
    try:
        parsed = json.loads(prompt)
    except json.JSONDecodeError as exc:
        raise click.BadParameter("PROMPT must be a valid JSON object or plain text.") from exc
    if not isinstance(parsed, dict):
        raise click.BadParameter("PROMPT must be a JSON object or plain text.")
    return parsed


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

    PROMPT is a description of the lyrics to generate, or a JSON object matching the API schema.

    \b
    Examples:
      producer lyrics "A love song about the ocean at sunset"
      producer lyrics "Funny rap about programming bugs"
      producer lyrics "Epic ballad about adventure and discovery"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_lyrics(prompt=_parse_prompt(prompt))
        if output_json:
            print_json(result)
        else:
            print_lyrics_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e

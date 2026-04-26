"""Generate content command using native Gemini API."""

import click

from gemini_cli.core.client import get_client
from gemini_cli.core.exceptions import GeminiError
from gemini_cli.core.output import (
    DEFAULT_MODEL,
    MODELS,
    print_error,
    print_generate_result,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Gemini model to use for content generation.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    output_json: bool,
) -> None:
    """Generate content using the native Gemini API.

    PROMPT is the text to send to the model.

    \b
    Examples:
      gemini-cli generate "What is the capital of France?"
      gemini-cli generate "Explain quantum computing" -m gemini-2.5-pro
      gemini-cli generate "Write a haiku" --json
    """
    client = get_client(ctx.obj.get("token"))
    contents = [{"parts": [{"text": prompt}]}]

    try:
        result = client.generate_content(model=model, contents=contents)
        if output_json:
            print_json(result)
        else:
            print_generate_result(result)
    except GeminiError as e:
        print_error(e.message)
        raise SystemExit(1) from e

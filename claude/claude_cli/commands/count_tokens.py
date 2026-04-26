"""Count tokens command."""

import click

from claude_cli.core.client import get_client
from claude_cli.core.exceptions import ClaudeError
from claude_cli.core.output import (
    DEFAULT_MODEL,
    MODELS,
    print_error,
    print_json,
    print_token_count_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Claude model to count tokens for.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def count_tokens(
    ctx: click.Context,
    prompt: str,
    model: str,
    output_json: bool,
) -> None:
    """Count the number of tokens in a message.

    PROMPT is the user message to count tokens for.

    \b
    Examples:
      claude-cli count-tokens "What is the capital of France?"
      claude-cli count-tokens "Hello" -m claude-opus-4-20250514
      claude-cli count-tokens "Some text" --json
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        result = client.count_tokens(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_token_count_result(result)
    except ClaudeError as e:
        print_error(e.message)
        raise SystemExit(1) from e

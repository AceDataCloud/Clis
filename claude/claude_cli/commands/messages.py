"""Messages command using native Claude Messages API."""

import click

from claude_cli.core.client import get_client
from claude_cli.core.exceptions import ClaudeError
from claude_cli.core.output import (
    DEFAULT_MODEL,
    MODELS,
    print_error,
    print_json,
    print_messages_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Claude model to use.",
)
@click.option(
    "--max-tokens",
    default=1024,
    type=int,
    show_default=True,
    help="Maximum number of tokens to generate.",
)
@click.option(
    "-s",
    "--system",
    default=None,
    help="System prompt to set the assistant's behavior.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def messages(
    ctx: click.Context,
    prompt: str,
    model: str,
    max_tokens: int,
    system: str | None,
    output_json: bool,
) -> None:
    """Send a message using the native Claude Messages API.

    PROMPT is the user message to send to the model.

    \b
    Examples:
      claude-cli messages "What is the capital of France?"
      claude-cli messages "Explain AI" -m claude-opus-4-20250514
      claude-cli messages "Summarize this" -s "You are a concise summarizer"
      claude-cli messages "Hello" --max-tokens 2048
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    if system:
        payload["system"] = system

    try:
        result = client.messages(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_messages_result(result)
    except ClaudeError as e:
        print_error(e.message)
        raise SystemExit(1) from e

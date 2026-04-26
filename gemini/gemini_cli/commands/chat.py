"""Chat completion command."""

import click

from gemini_cli.core.client import get_client
from gemini_cli.core.exceptions import GeminiError
from gemini_cli.core.output import (
    DEFAULT_MODEL,
    MODELS,
    print_chat_result,
    print_error,
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
    help="Model to use for chat completion.",
)
@click.option(
    "-s",
    "--system",
    default=None,
    help="System prompt to set the assistant's behavior.",
)
@click.option(
    "--temperature",
    default=None,
    type=float,
    help="Sampling temperature (0-2). Higher values = more random.",
)
@click.option(
    "--max-tokens",
    default=None,
    type=int,
    help="Maximum number of tokens to generate.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def chat(
    ctx: click.Context,
    prompt: str,
    model: str,
    system: str | None,
    temperature: float | None,
    max_tokens: int | None,
    output_json: bool,
) -> None:
    """Chat with a Gemini model.

    PROMPT is the user message to send to the model.

    \b
    Examples:
      gemini-cli chat "What is the capital of France?"
      gemini-cli chat "Explain AI" -m gemini-2.5-pro
      gemini-cli chat "Write a poem" --temperature 0.9
      gemini-cli chat "Summarize this" -s "You are a concise summarizer"
    """
    client = get_client(ctx.obj.get("token"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload: dict[str, object] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        result = client.chat_completions(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except GeminiError as e:
        print_error(e.message)
        raise SystemExit(1) from e

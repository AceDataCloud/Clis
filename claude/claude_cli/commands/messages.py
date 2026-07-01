"""Claude Messages API commands (native Claude endpoint)."""

import click

from claude_cli.core.client import get_client
from claude_cli.core.exceptions import ClaudeError
from claude_cli.core.output import (
    DEFAULT_MESSAGES_MODEL,
    MESSAGES_MODELS,
    print_count_tokens_result,
    print_error,
    print_json,
    print_messages_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(MESSAGES_MODELS),
    default=DEFAULT_MESSAGES_MODEL,
    show_default=True,
    help="Model to use.",
)
@click.option(
    "--max-tokens",
    default=1024,
    type=int,
    show_default=True,
    help="Maximum number of tokens to generate (required by the API).",
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
    help="Sampling temperature (0-1). Higher values = more random.",
)
@click.option(
    "--top-p",
    default=None,
    type=float,
    help="Nucleus sampling probability mass (0-1). Alternative to temperature.",
)
@click.option(
    "--top-k",
    default=None,
    type=int,
    help="Only sample from top K options for each token.",
)
@click.option(
    "--stop-sequences",
    default=None,
    multiple=True,
    help="Stop sequence(s) where the API will stop generating (repeatable).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def messages(
    ctx: click.Context,
    prompt: str,
    model: str,
    max_tokens: int,
    system: str | None,
    temperature: float | None,
    top_p: float | None,
    top_k: int | None,
    stop_sequences: tuple[str, ...],
    output_json: bool,
) -> None:
    """Send a message using the Claude native Messages API.

    PROMPT is the user message to send to the model.

    \b
    Examples:
      claude messages "What is the capital of France?"
      claude messages "Tell me a joke" -m claude-3-5-sonnet-20241022
      claude messages "Explain AI" --max-tokens 2048
      claude messages "Summarize this" -s "You are a concise summarizer"
    """
    client = get_client(ctx.obj.get("token"))
    msg_list = [{"role": "user", "content": prompt}]

    payload: dict[str, object] = {
        "model": model,
        "messages": msg_list,
        "max_tokens": max_tokens,
        "system": system,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "stop_sequences": list(stop_sequences) if stop_sequences else None,
    }

    try:
        result = client.messages(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_messages_result(result)
    except ClaudeError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command(name="count-tokens")
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(MESSAGES_MODELS),
    default=DEFAULT_MESSAGES_MODEL,
    show_default=True,
    help="Model to use for token counting.",
)
@click.option(
    "-s",
    "--system",
    default=None,
    help="System prompt to include in token count.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def count_tokens(
    ctx: click.Context,
    prompt: str,
    model: str,
    system: str | None,
    output_json: bool,
) -> None:
    """Count tokens for a Claude Messages API request.

    PROMPT is the user message to count tokens for.

    \b
    Examples:
      claude count-tokens "What is the capital of France?"
      claude count-tokens "Hello" -m claude-3-5-sonnet-20241022
      claude count-tokens "Summarize this" -s "You are a summarizer"
    """
    client = get_client(ctx.obj.get("token"))
    msg_list = [{"role": "user", "content": prompt}]

    payload: dict[str, object] = {
        "model": model,
        "messages": msg_list,
        "system": system,
    }

    try:
        result = client.count_tokens(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_count_tokens_result(result)
    except ClaudeError as e:
        print_error(e.message)
        raise SystemExit(1) from e

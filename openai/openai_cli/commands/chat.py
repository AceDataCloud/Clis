"""Chat completion commands."""

import json

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    CHAT_MODELS,
    DEFAULT_CHAT_MODEL,
    print_chat_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("message")
@click.option(
    "-m",
    "--model",
    type=click.Choice(CHAT_MODELS),
    default=DEFAULT_CHAT_MODEL,
    help="Model to use for chat completion.",
)
@click.option(
    "-s",
    "--system",
    default=None,
    help="System prompt to set assistant behavior.",
)
@click.option(
    "-t",
    "--temperature",
    type=float,
    default=None,
    help="Sampling temperature between 0 and 2 (default: 1).",
)
@click.option(
    "--max-tokens",
    type=int,
    default=None,
    help="Maximum number of tokens to generate.",
)
@click.option(
    "-n",
    "--number",
    type=int,
    default=None,
    help="How many completion choices to generate (default: 1).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def chat(
    ctx: click.Context,
    message: str,
    model: str,
    system: str | None,
    temperature: float | None,
    max_tokens: int | None,
    number: int | None,
    output_json: bool,
) -> None:
    """Send a chat message and get a completion.

    MESSAGE is the user message to send.

    \b
    Examples:
      openai chat "What is the capital of France?"
      openai chat "Explain quantum computing" -m gpt-4o
      openai chat "Write a haiku" -m gpt-5 --temperature 1.5
      openai chat "Summarize this" -s "You are a concise summarizer"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})

        payload: dict[str, object] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "n": number,
        }

        result = client.chat(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("messages_json")
@click.option(
    "-m",
    "--model",
    type=click.Choice(CHAT_MODELS),
    default=DEFAULT_CHAT_MODEL,
    help="Model to use for chat completion.",
)
@click.option(
    "-t",
    "--temperature",
    type=float,
    default=None,
    help="Sampling temperature between 0 and 2 (default: 1).",
)
@click.option(
    "--max-tokens",
    type=int,
    default=None,
    help="Maximum number of tokens to generate.",
)
@click.option(
    "-n",
    "--number",
    type=int,
    default=None,
    help="How many completion choices to generate (default: 1).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def complete(
    ctx: click.Context,
    messages_json: str,
    model: str,
    temperature: float | None,
    max_tokens: int | None,
    number: int | None,
    output_json: bool,
) -> None:
    """Create a chat completion from a JSON messages array.

    MESSAGES_JSON is a JSON array of message objects with 'role' and 'content'.

    \b
    Examples:
      openai complete '[{"role":"user","content":"Hello"}]'
      openai complete '[{"role":"system","content":"Be concise"},{"role":"user","content":"Hi"}]' -m gpt-4o
    """
    client = get_client(ctx.obj.get("token"))
    try:
        messages = json.loads(messages_json)
        payload: dict[str, object] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "n": number,
        }

        result = client.chat(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except (json.JSONDecodeError, ValueError) as e:
        print_error(f"Invalid messages JSON: {e}")
        raise SystemExit(1) from e
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

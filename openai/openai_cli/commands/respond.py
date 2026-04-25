"""Responses API commands."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_RESPONSES_MODEL,
    RESPONSES_MODELS,
    print_chat_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("message")
@click.option(
    "-m",
    "--model",
    type=click.Choice(RESPONSES_MODELS),
    default=DEFAULT_RESPONSES_MODEL,
    help="Model to use for the response.",
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
    help="How many response choices to generate (default: 1).",
)
@click.option(
    "--background",
    is_flag=True,
    default=False,
    help="Run the model response in the background.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def respond(
    ctx: click.Context,
    message: str,
    model: str,
    temperature: float | None,
    max_tokens: int | None,
    number: int | None,
    background: bool,
    output_json: bool,
) -> None:
    """Create a response using the OpenAI Responses API.

    MESSAGE is the user message to send.

    \b
    Examples:
      openai respond "What is the capital of France?"
      openai respond "Explain quantum computing" -m gpt-4o
      openai respond "Summarize this" -m o3
    """
    client = get_client(ctx.obj.get("token"))
    try:
        input_messages: list[dict[str, str]] = [{"role": "user", "content": message}]

        payload: dict[str, object] = {
            "model": model,
            "input": input_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "n": number,
            "background": background if background else None,
        }

        result = client.respond(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

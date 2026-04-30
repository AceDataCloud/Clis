"""Responses API command."""

import json as json_module

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_RESPONSE_MODEL,
    RESPONSE_MODELS,
    print_error,
    print_json,
    print_response_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(RESPONSE_MODELS),
    default=DEFAULT_RESPONSE_MODEL,
    show_default=True,
    help="Model to use for the response.",
)
@click.option(
    "--temperature",
    default=None,
    type=float,
    help="Sampling temperature (0-2).",
)
@click.option(
    "--max-tokens",
    default=None,
    type=int,
    help="Maximum number of tokens to generate.",
)
@click.option(
    "-n",
    "--count",
    default=None,
    type=int,
    help="Number of completion choices to generate.",
)
@click.option(
    "--response-format",
    default=None,
    help="Response format as JSON string (e.g. '{\"type\": \"json_object\"}').",
)
@click.option(
    "--background",
    is_flag=True,
    default=False,
    help="Run the response in the background.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def response(
    ctx: click.Context,
    prompt: str,
    model: str,
    temperature: float | None,
    max_tokens: int | None,
    count: int | None,
    response_format: str | None,
    background: bool,
    output_json: bool,
) -> None:
    """Send a request to the Responses API.

    PROMPT is the user input message.

    \b
    Examples:
      openai-cli response "Summarize the latest AI news"
      openai-cli response "What is 2+2?" -m gpt-5.4
      openai-cli response "Write a haiku" --temperature 1.2
    """
    client = get_client(ctx.obj.get("token"))
    parsed_response_format = None
    if response_format:
        try:
            parsed_response_format = json_module.loads(response_format)
        except json_module.JSONDecodeError:
            print_error(f"Invalid JSON for --response-format: {response_format}")
            raise SystemExit(1)
    payload: dict[str, object] = {
        "model": model,
        "input": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "n": count,
        "response_format": parsed_response_format,
        "background": background if background else None,
    }

    try:
        result = client.responses(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_response_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

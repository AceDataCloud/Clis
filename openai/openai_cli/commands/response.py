"""Responses API command."""

import click

from openai_cli.commands._json import parse_json_array, parse_json_object, parse_json_or_string
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
    help='Response format as JSON string (e.g. \'{"type": "json_object"}\').',
)
@click.option(
    "--tools",
    default=None,
    help='Tool definitions as a JSON array (e.g. \'[{"type":"web_search_preview"}]\').',
)
@click.option(
    "--tool-choice",
    default=None,
    help='Tool choice mode or JSON object (e.g. "auto" or \'{"type":"function","function":{"name":"lookup"}}\').',
)
@click.option(
    "--include",
    "include_fields",
    multiple=True,
    help="Additional output fields to include (repeatable).",
)
@click.option("--stream", is_flag=True, default=False, help="Stream partial response events.")
@click.option(
    "--background",
    is_flag=True,
    default=False,
    help="Run the response in the background.",
)
@click.option(
    "--max-output-tokens",
    default=None,
    type=int,
    help="Maximum number of output tokens to generate.",
)
@click.option(
    "--parallel-tool-calls",
    "parallel_tool_calls",
    flag_value=True,
    default=None,
    help="Enable parallel function calling during tool use.",
)
@click.option(
    "--no-parallel-tool-calls",
    "parallel_tool_calls",
    flag_value=False,
    help="Disable parallel function calling during tool use.",
)
@click.option(
    "--reasoning",
    default=None,
    help="Reasoning settings as a JSON object.",
)
@click.option(
    "--text",
    default=None,
    help="Text generation settings as a JSON object.",
)
@click.option(
    "--stream-options",
    default=None,
    help="Streaming options as a JSON object.",
)
@click.option(
    "--store",
    is_flag=True,
    default=False,
    help="Store the output for use in OpenAI's model distillation or evals products.",
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
    tools: str | None,
    tool_choice: str | None,
    include_fields: tuple[str, ...],
    stream: bool,
    background: bool,
    max_output_tokens: int | None,
    parallel_tool_calls: bool | None,
    reasoning: str | None,
    text: str | None,
    stream_options: str | None,
    store: bool,
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
    try:
        parsed_response_format = parse_json_object(response_format, "--response-format")
        parsed_tools = parse_json_array(tools, "--tools")
        parsed_tool_choice = parse_json_or_string(tool_choice, "--tool-choice")
        parsed_reasoning = parse_json_object(reasoning, "--reasoning")
        parsed_text = parse_json_object(text, "--text")
        parsed_stream_options = parse_json_object(stream_options, "--stream-options")
    except click.BadParameter as e:
        print_error(e.format_message())
        raise SystemExit(1) from None
    payload: dict[str, object] = {
        "model": model,
        "input": [{"role": "user", "content": prompt}],
        "stream": stream or None,
        "tools": parsed_tools,
        "tool_choice": parsed_tool_choice,
        "include": list(include_fields) if include_fields else None,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_output_tokens": max_output_tokens,
        "n": count,
        "response_format": parsed_response_format,
        "background": background if background else None,
        "parallel_tool_calls": parallel_tool_calls,
        "reasoning": parsed_reasoning,
        "text": parsed_text,
        "stream_options": parsed_stream_options,
        "store": store if store else None,
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

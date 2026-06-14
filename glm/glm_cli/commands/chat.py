"""Chat completion command."""

import json
from typing import Any, Literal

import click

from glm_cli.core.client import get_client
from glm_cli.core.exceptions import GLMError
from glm_cli.core.output import (
    DEFAULT_MODEL,
    GLM_MODELS,
    print_chat_result,
    print_error,
    print_json,
)


def _parse_json_option(
    option_name: str,
    value: str | None,
    expected_kind: Literal["object", "array"],
) -> Any | None:
    if value is None:
        return None

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        print_error(f"Invalid JSON for --{option_name}.")
        raise SystemExit(1) from None

    expected_type = dict if expected_kind == "object" else list
    if not isinstance(parsed, expected_type):
        print_error(f"--{option_name} must be a JSON {expected_kind}.")
        raise SystemExit(1)

    return parsed


def _parse_tool_choice(value: str | None) -> str | dict[str, Any] | None:
    if value in {None, "none", "auto", "required"}:
        return value

    return _parse_json_option("tool-choice", value, "object")


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(GLM_MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="GLM model to use for chat completion.",
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
@click.option(
    "--stream/--no-stream",
    default=None,
    help="Enable or disable streaming responses.",
)
@click.option(
    "--response-format",
    default=None,
    help='Response format as JSON (e.g. \'{"type":"json_object"}\').',
)
@click.option(
    "--max-completion-tokens",
    default=None,
    type=int,
    help="Upper bound for tokens generated in a completion.",
)
@click.option(
    "-n",
    "--count",
    default=None,
    type=int,
    help="Number of completion choices to generate.",
)
@click.option(
    "--top-p",
    default=None,
    type=float,
    help="Nucleus sampling probability mass (0-1).",
)
@click.option(
    "--frequency-penalty",
    default=None,
    type=float,
    help="Penalize tokens by their frequency in the text so far (-2.0 to 2.0).",
)
@click.option(
    "--presence-penalty",
    default=None,
    type=float,
    help="Penalize tokens that have already appeared in the text (-2.0 to 2.0).",
)
@click.option(
    "--seed",
    default=None,
    type=int,
    help="Seed for deterministic sampling.",
)
@click.option(
    "--logprobs/--no-logprobs",
    default=None,
    help="Return log probabilities of output tokens.",
)
@click.option(
    "--top-logprobs",
    default=None,
    type=click.IntRange(0, 20),
    help="Number of most likely tokens (0-20) to return with log probabilities.",
)
@click.option(
    "--stream-options",
    default=None,
    help='Streaming options as JSON (e.g. \'{"include_usage":true}\').',
)
@click.option(
    "--stop",
    default=None,
    multiple=True,
    help="Stop sequence(s) where the API will stop generating (repeatable, up to 4).",
)
@click.option(
    "--parallel-tool-calls/--no-parallel-tool-calls",
    default=None,
    help="Enable or disable parallel tool calling.",
)
@click.option(
    "--reasoning-effort",
    type=click.Choice(["minimal", "low", "medium", "high"]),
    default=None,
    help="Reasoning effort level for supported models.",
)
@click.option(
    "--user",
    default=None,
    help="Unique end-user identifier for monitoring and abuse detection.",
)
@click.option(
    "--service-tier",
    type=click.Choice(["auto", "default", "flex", "scale", "priority"]),
    default=None,
    help="Processing tier for the request.",
)
@click.option(
    "--store/--no-store",
    default=None,
    help="Enable or disable output storage for the request.",
)
@click.option(
    "--metadata",
    default=None,
    help='Metadata as a JSON object (e.g. \'{"team":"cli"}\').',
)
@click.option(
    "--logit-bias",
    default=None,
    help='Logit bias as a JSON object (e.g. \'{"50256":-100}\').',
)
@click.option(
    "--modality",
    "modalities",
    multiple=True,
    type=click.Choice(["text", "audio"]),
    help="Output modality to request (repeatable).",
)
@click.option(
    "--audio",
    default=None,
    help='Audio output settings as JSON (e.g. \'{"voice":"alloy","format":"mp3"}\').',
)
@click.option(
    "--prediction",
    default=None,
    help='Prediction configuration as JSON.',
)
@click.option(
    "--web-search-options",
    default=None,
    help='Web search options as JSON.',
)
@click.option(
    "--tools",
    default=None,
    help='Tool definitions as a JSON array.',
)
@click.option(
    "--tool-choice",
    default=None,
    help='Tool choice as `auto`, `none`, `required`, or a JSON object.',
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
    stream: bool | None,
    response_format: str | None,
    max_completion_tokens: int | None,
    count: int | None,
    top_p: float | None,
    frequency_penalty: float | None,
    presence_penalty: float | None,
    seed: int | None,
    logprobs: bool | None,
    top_logprobs: int | None,
    stream_options: str | None,
    stop: tuple[str, ...],
    parallel_tool_calls: bool | None,
    reasoning_effort: str | None,
    user: str | None,
    service_tier: str | None,
    store: bool | None,
    metadata: str | None,
    logit_bias: str | None,
    modalities: tuple[str, ...],
    audio: str | None,
    prediction: str | None,
    web_search_options: str | None,
    tools: str | None,
    tool_choice: str | None,
    output_json: bool,
) -> None:
    """Chat with a GLM model.

    PROMPT is the user message to send to the model.

    \b
    Examples:
      glm chat "What is the capital of France?"
      glm chat "Explain quantum computing" -m glm-5.1
      glm chat "Write a poem" --temperature 0.9
      glm chat "Summarize this" -s "You are a concise summarizer"
    """
    client = get_client(ctx.obj.get("token"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    parsed_response_format = _parse_json_option("response-format", response_format, "object")
    parsed_stream_options = _parse_json_option("stream-options", stream_options, "object")
    parsed_metadata = _parse_json_option("metadata", metadata, "object")
    parsed_logit_bias = _parse_json_option("logit-bias", logit_bias, "object")
    parsed_audio = _parse_json_option("audio", audio, "object")
    parsed_prediction = _parse_json_option("prediction", prediction, "object")
    parsed_web_search_options = _parse_json_option(
        "web-search-options", web_search_options, "object"
    )
    parsed_tools = _parse_json_option("tools", tools, "array")
    parsed_tool_choice = _parse_tool_choice(tool_choice)

    payload: dict[str, object] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
        "response_format": parsed_response_format,
        "max_completion_tokens": max_completion_tokens,
        "n": count,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "seed": seed,
        "logprobs": logprobs,
        "top_logprobs": top_logprobs,
        "stream_options": parsed_stream_options,
        "stop": list(stop) if stop else None,
        "parallel_tool_calls": parallel_tool_calls,
        "reasoning_effort": reasoning_effort,
        "user": user,
        "service_tier": service_tier,
        "store": store,
        "metadata": parsed_metadata,
        "logit_bias": parsed_logit_bias,
        "modalities": list(modalities) if modalities else None,
        "audio": parsed_audio,
        "prediction": parsed_prediction,
        "web_search_options": parsed_web_search_options,
        "tools": parsed_tools,
        "tool_choice": parsed_tool_choice,
    }

    try:
        result = client.chat_completions(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except GLMError as e:
        print_error(e.message)
        raise SystemExit(1) from e

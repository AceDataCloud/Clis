"""Chat completion command."""

import click

from gemini_cli.commands._json import (
    parse_json_array,
    parse_json_object,
    parse_json_or_string,
)
from gemini_cli.core.client import get_client
from gemini_cli.core.exceptions import GeminiError
from gemini_cli.core.output import (
    DEFAULT_CHAT_MODEL,
    GEMINI_CHAT_MODELS,
    print_chat_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(GEMINI_CHAT_MODELS),
    default=DEFAULT_CHAT_MODEL,
    show_default=True,
    help="Gemini model to use for chat completion.",
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
    "--stop",
    default=None,
    multiple=True,
    help="Stop sequence(s) where the API will stop generating (repeatable, up to 4).",
)
@click.option(
    "--reasoning-effort",
    type=click.Choice(["minimal", "low", "medium", "high"]),
    default=None,
    help="Reasoning effort level.",
)
@click.option(
    "--max-completion-tokens",
    default=None,
    type=int,
    help="Maximum number of tokens to generate (alternative to --max-tokens).",
)
@click.option(
    "--service-tier",
    type=click.Choice(["auto", "default", "flex", "scale", "priority"]),
    default=None,
    help="Service tier for compute allocation.",
)
@click.option(
    "--user",
    default=None,
    help="Unique end-user identifier for monitoring and abuse detection.",
)
@click.option(
    "--store",
    is_flag=True,
    default=False,
    help="Store the output for model distillation or evals.",
)
@click.option(
    "--logprobs",
    is_flag=True,
    default=False,
    help="Return log probabilities of the output tokens.",
)
@click.option(
    "--top-logprobs",
    default=None,
    type=click.IntRange(0, 20),
    help="Number of most likely tokens (0-20) to return at each token position with log probabilities.",
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
@click.option("--stream", is_flag=True, default=False, help="Stream partial chat completion events.")
@click.option(
    "--response-format",
    default=None,
    help='Response format as JSON (e.g. \'{"type": "json_schema", "json_schema": {...}}\').',
)
@click.option(
    "--tools",
    default=None,
    help='Tool definitions as a JSON array (e.g. \'[{"type":"function","function":{...}}]\').',
)
@click.option(
    "--tool-choice",
    default=None,
    help='Tool selection mode or JSON object (e.g. "auto" or \'{"type":"function","function":{"name":"lookup"}}\').',
)
@click.option(
    "--stream-options",
    default=None,
    help='Streaming options as a JSON object (e.g. \'{"include_usage": true}\').',
)
@click.option(
    "--metadata",
    default=None,
    help="Metadata as a JSON object.",
)
@click.option(
    "--logit-bias",
    default=None,
    help="Logit bias map as a JSON object.",
)
@click.option(
    "--modalities",
    default=None,
    help="Requested modalities as a JSON array.",
)
@click.option(
    "--audio",
    default=None,
    help="Audio output settings as a JSON object.",
)
@click.option(
    "--prediction",
    default=None,
    help="Prediction settings as a JSON object.",
)
@click.option(
    "--web-search-options",
    default=None,
    help="Web search settings as a JSON object.",
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
    count: int | None,
    top_p: float | None,
    frequency_penalty: float | None,
    presence_penalty: float | None,
    seed: int | None,
    stop: tuple[str, ...],
    reasoning_effort: str | None,
    max_completion_tokens: int | None,
    service_tier: str | None,
    user: str | None,
    store: bool,
    logprobs: bool,
    top_logprobs: int | None,
    parallel_tool_calls: bool | None,
    stream: bool,
    response_format: str | None,
    tools: str | None,
    tool_choice: str | None,
    stream_options: str | None,
    metadata: str | None,
    logit_bias: str | None,
    modalities: str | None,
    audio: str | None,
    prediction: str | None,
    web_search_options: str | None,
    output_json: bool,
) -> None:
    """Chat with a Gemini model.

    PROMPT is the user message to send to the model.

    \b
    Examples:
      gemini chat "What is the capital of France?"
      gemini chat "Explain quantum computing" -m gemini-2.5-pro
      gemini chat "Write a poem" --temperature 0.9
      gemini chat "Summarize this" -s "You are a concise summarizer"
    """
    client = get_client(ctx.obj.get("token"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        parsed_response_format = parse_json_object(response_format, "--response-format")
        parsed_tools = parse_json_array(tools, "--tools")
        parsed_tool_choice = parse_json_or_string(tool_choice, "--tool-choice")
        parsed_stream_options = parse_json_object(stream_options, "--stream-options")
        parsed_metadata = parse_json_object(metadata, "--metadata")
        parsed_logit_bias = parse_json_object(logit_bias, "--logit-bias")
        parsed_modalities = parse_json_array(modalities, "--modalities")
        parsed_audio = parse_json_object(audio, "--audio")
        parsed_prediction = parse_json_object(prediction, "--prediction")
        parsed_web_search_options = parse_json_object(web_search_options, "--web-search-options")
    except click.BadParameter as e:
        print_error(e.format_message())
        raise SystemExit(1) from None

    payload: dict[str, object] = {
        "model": model,
        "messages": messages,
        "stream": stream or None,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_completion_tokens": max_completion_tokens,
        "n": count,
        "response_format": parsed_response_format,
        "tools": parsed_tools,
        "tool_choice": parsed_tool_choice,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "seed": seed,
        "stop": list(stop) if stop else None,
        "stream_options": parsed_stream_options,
        "reasoning_effort": reasoning_effort,
        "service_tier": service_tier,
        "user": user,
        "store": store if store else None,
        "metadata": parsed_metadata,
        "logit_bias": parsed_logit_bias,
        "logprobs": logprobs if logprobs else None,
        "top_logprobs": top_logprobs,
        "parallel_tool_calls": parallel_tool_calls,
        "modalities": parsed_modalities,
        "audio": parsed_audio,
        "prediction": parsed_prediction,
        "web_search_options": parsed_web_search_options,
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

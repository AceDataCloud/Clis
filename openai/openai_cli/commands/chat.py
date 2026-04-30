"""Chat completion command."""

import json as json_module

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
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(CHAT_MODELS),
    default=DEFAULT_CHAT_MODEL,
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
@click.option(
    "--max-completion-tokens",
    default=None,
    type=int,
    help="Upper bound for tokens generated in a completion (including reasoning tokens).",
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
    help="Nucleus sampling probability mass (0-1). Alternative to temperature.",
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
    help="Reasoning effort for o1/o3/o4/gpt-5 series models.",
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
    help="Processing type for serving the request (auto, default, flex, scale, priority).",
)
@click.option(
    "--response-format",
    default=None,
    help="Response format as JSON string (e.g. '{\"type\": \"json_object\"}').",
)
@click.option(
    "--logprobs",
    is_flag=True,
    default=False,
    help="Return log probabilities of output tokens.",
)
@click.option(
    "--top-logprobs",
    default=None,
    type=click.IntRange(0, 20),
    help="Number of most likely tokens to return log probs for (0-20, requires --logprobs).",
)
@click.option(
    "--parallel-tool-calls/--no-parallel-tool-calls",
    default=None,
    help="Enable or disable parallel function calling during tool use.",
)
@click.option(
    "--store",
    is_flag=True,
    default=False,
    help="Store the output of this chat completion.",
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
    max_completion_tokens: int | None,
    count: int | None,
    top_p: float | None,
    frequency_penalty: float | None,
    presence_penalty: float | None,
    seed: int | None,
    stop: tuple[str, ...],
    reasoning_effort: str | None,
    user: str | None,
    service_tier: str | None,
    response_format: str | None,
    logprobs: bool,
    top_logprobs: int | None,
    parallel_tool_calls: bool | None,
    store: bool,
    output_json: bool,
) -> None:
    """Chat with an OpenAI-compatible model.

    PROMPT is the user message to send to the model.

    \b
    Examples:
      openai-cli chat "What is the capital of France?"
      openai-cli chat "Explain quantum computing" -m gpt-5.4
      openai-cli chat "Write a poem" -m gpt-4o --temperature 0.9
      openai-cli chat "Summarize this" -s "You are a concise summarizer"
      openai-cli chat "Reason about this" -m o3 --reasoning-effort high
    """
    client = get_client(ctx.obj.get("token"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    parsed_response_format = None
    if response_format:
        try:
            parsed_response_format = json_module.loads(response_format)
        except json_module.JSONDecodeError:
            print_error(f"Invalid JSON for --response-format: {response_format}")
            raise SystemExit(1)

    payload: dict[str, object] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_completion_tokens": max_completion_tokens,
        "n": count,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "seed": seed,
        "stop": list(stop) if stop else None,
        "reasoning_effort": reasoning_effort,
        "user": user,
        "service_tier": service_tier,
        "response_format": parsed_response_format,
        "logprobs": logprobs or None,
        "top_logprobs": top_logprobs,
        "parallel_tool_calls": parallel_tool_calls,
        "store": store or None,
    }

    try:
        result = client.chat_completions(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

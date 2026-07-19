"""Chat completion command."""

import click

from kimi_cli.core.client import get_client
from kimi_cli.core.exceptions import KimiError
from kimi_cli.core.output import (
    DEFAULT_MODEL,
    KIMI_MODELS,
    REASONING_EFFORTS,
    SERVICE_TIERS,
    print_chat_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(KIMI_MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Kimi model to use for chat completion.",
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
    "--user",
    default=None,
    help="Unique end-user identifier for monitoring and abuse detection.",
)
@click.option(
    "--reasoning-effort",
    default=None,
    type=click.Choice(REASONING_EFFORTS),
    help="Reasoning effort level (max).",
)
@click.option(
    "--service-tier",
    default=None,
    type=click.Choice(SERVICE_TIERS),
    help="Service tier for the request (auto/default/flex/scale/priority).",
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
    type=int,
    help="Number of most likely tokens (with log probabilities) to return at each position.",
)
@click.option(
    "--max-completion-tokens",
    default=None,
    type=int,
    help="Upper bound on the number of tokens that can be generated for a completion.",
)
@click.option(
    "--parallel-tool-calls",
    "parallel_tool_calls",
    is_flag=True,
    default=False,
    help="Enable parallel function calling during tool use.",
)
@click.option(
    "--store",
    is_flag=True,
    default=False,
    help="Whether to store the output of this completion request.",
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
    user: str | None,
    reasoning_effort: str | None,
    service_tier: str | None,
    logprobs: bool,
    top_logprobs: int | None,
    max_completion_tokens: int | None,
    parallel_tool_calls: bool,
    store: bool,
    output_json: bool,
) -> None:
    """Chat with a Kimi model.

    PROMPT is the user message to send to the model.

    \b
    Examples:
      kimi chat "What is the capital of France?"
      kimi chat "Explain quantum computing" -m kimi-k3
      kimi chat "Write a poem" --temperature 0.9
      kimi chat "Summarize this" -s "You are a concise summarizer"
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
        "n": count,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "seed": seed,
        "stop": list(stop) if stop else None,
        "user": user,
        "reasoning_effort": reasoning_effort,
        "service_tier": service_tier,
        "logprobs": logprobs or None,
        "top_logprobs": top_logprobs,
        "max_completion_tokens": max_completion_tokens,
        "parallel_tool_calls": parallel_tool_calls or None,
        "store": store or None,
    }

    try:
        result = client.chat_completions(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except KimiError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Chat completion command."""

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
    "-n",
    "--count",
    default=None,
    type=int,
    help="Number of completion choices to generate.",
)
@click.option(
    "--reasoning-effort",
    type=click.Choice(["minimal", "low", "medium", "high"]),
    default=None,
    help="Reasoning effort for o1/o3/o4/gpt-5 series models.",
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
    reasoning_effort: str | None,
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
        "reasoning_effort": reasoning_effort,
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

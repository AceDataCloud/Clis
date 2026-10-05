"""Claude Messages API commands (native Claude endpoint)."""

import click

from claude_cli.commands._json import parse_json_array, parse_json_object
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
@click.option(
    "--thinking-type",
    type=str,
    default=None,
    help="Thinking mode passed through to the model (e.g. adaptive, enabled, disabled).",
)
@click.option(
    "--thinking-budget-tokens",
    default=None,
    type=int,
    help="Thinking token budget passed through to the model.",
)
@click.option(
    "--thinking-display",
    type=str,
    default=None,
    help="Thinking display mode passed through to the model (e.g. summarized, omitted, updates).",
)
@click.option("--thinking", default=None, help="Thinking configuration as a JSON object.")
@click.option(
    "--anthropic-beta",
    default=None,
    help="Anthropic beta header value (comma-separated for multiple betas).",
)
@click.option("--metadata", default=None, help="Request metadata as a JSON object.")
@click.option("--stream", is_flag=True, default=False, help="Stream incremental events.")
@click.option("--tools", default=None, help="Tool definitions as a JSON array.")
@click.option("--tool-choice", default=None, help="Tool choice as a JSON object.")
@click.option("--output-config", default=None, help="Output configuration as a JSON object.")
@click.option("--cache-control", default=None, help="Cache control as a JSON object.")
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
    thinking_type: str | None,
    thinking_budget_tokens: int | None,
    thinking_display: str | None,
    thinking: str | None,
    anthropic_beta: str | None,
    metadata: str | None,
    stream: bool,
    tools: str | None,
    tool_choice: str | None,
    output_config: str | None,
    cache_control: str | None,
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
      claude messages "Think deeply" --thinking-type enabled --thinking-budget-tokens 2048
    """
    client = get_client(ctx.obj.get("token"))
    msg_list = [{"role": "user", "content": prompt}]

    try:
        parsed_thinking = parse_json_object(thinking, "--thinking")
        thinking_options = {
            "type": thinking_type,
            "budget_tokens": thinking_budget_tokens,
            "display": thinking_display,
        }
        for key, value in thinking_options.items():
            if value is not None:
                if parsed_thinking is None:
                    parsed_thinking = {}
                parsed_thinking[key] = value
        parsed_metadata = parse_json_object(metadata, "--metadata")
        parsed_tools = parse_json_array(tools, "--tools")
        parsed_tool_choice = parse_json_object(tool_choice, "--tool-choice")
        parsed_output_config = parse_json_object(output_config, "--output-config")
        parsed_cache_control = parse_json_object(cache_control, "--cache-control")
    except click.BadParameter as e:
        print_error(e.format_message())
        raise SystemExit(1) from None

    payload: dict[str, object] = {
        "model": model,
        "messages": msg_list,
        "max_tokens": max_tokens,
        "metadata": parsed_metadata,
        "system": system,
        "stream": stream or None,
        "temperature": temperature,
        "tool_choice": parsed_tool_choice,
        "tools": parsed_tools,
        "top_p": top_p,
        "top_k": top_k,
        "stop_sequences": list(stop_sequences) if stop_sequences else None,
        "thinking": parsed_thinking,
        "output_config": parsed_output_config,
        "cache_control": parsed_cache_control,
    }

    try:
        result = client.messages(anthropic_beta=anthropic_beta, **payload)  # type: ignore[arg-type]
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
@click.option(
    "--thinking-type",
    type=str,
    default=None,
    help="Thinking mode passed through to the model (e.g. adaptive, enabled, disabled).",
)
@click.option(
    "--thinking-budget-tokens",
    default=None,
    type=int,
    help="Thinking token budget passed through to the model.",
)
@click.option(
    "--thinking-display",
    type=str,
    default=None,
    help="Thinking display mode passed through to the model (e.g. summarized, omitted, updates).",
)
@click.option("--thinking", default=None, help="Thinking configuration as a JSON object.")
@click.option(
    "--anthropic-beta",
    default=None,
    help="Anthropic beta header value (comma-separated for multiple betas).",
)
@click.option("--tools", default=None, help="Tool definitions as a JSON array.")
@click.option("--tool-choice", default=None, help="Tool choice as a JSON object.")
@click.option("--cache-control", default=None, help="Cache control as a JSON object.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def count_tokens(
    ctx: click.Context,
    prompt: str,
    model: str,
    system: str | None,
    thinking_type: str | None,
    thinking_budget_tokens: int | None,
    thinking_display: str | None,
    thinking: str | None,
    anthropic_beta: str | None,
    tools: str | None,
    tool_choice: str | None,
    cache_control: str | None,
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

    try:
        parsed_thinking = parse_json_object(thinking, "--thinking")
        thinking_options = {
            "type": thinking_type,
            "budget_tokens": thinking_budget_tokens,
            "display": thinking_display,
        }
        for key, value in thinking_options.items():
            if value is not None:
                if parsed_thinking is None:
                    parsed_thinking = {}
                parsed_thinking[key] = value
        parsed_tools = parse_json_array(tools, "--tools")
        parsed_tool_choice = parse_json_object(tool_choice, "--tool-choice")
        parsed_cache_control = parse_json_object(cache_control, "--cache-control")
    except click.BadParameter as e:
        print_error(e.format_message())
        raise SystemExit(1) from None

    payload: dict[str, object] = {
        "model": model,
        "messages": msg_list,
        "system": system,
        "thinking": parsed_thinking,
        "tool_choice": parsed_tool_choice,
        "tools": parsed_tools,
        "cache_control": parsed_cache_control,
    }

    try:
        result = client.count_tokens(anthropic_beta=anthropic_beta, **payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_count_tokens_result(result)
    except ClaudeError as e:
        print_error(e.message)
        raise SystemExit(1) from e

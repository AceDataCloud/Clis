"""Unified Chat Completions without a provider-specific model allowlist."""

import click

from aichat_cli.core.client import get_client
from aichat_cli.core.exceptions import AichatError
from aichat_cli.core.output import print_error, print_json


@click.command()
@click.argument("prompt")
@click.option("-m", "--model", required=True, help="Explicit model ID supporting Chat Completions.")
@click.option(
    "--max-completion-tokens",
    type=click.IntRange(min=1),
    default=None,
    help="Optional output-token limit for models supporting this field.",
)
@click.option("-s", "--system", default=None, help="Optional system prompt.")
@click.option("--json", "output_json", is_flag=True, help="Output the complete JSON response.")
@click.pass_context
def completions(
    ctx: click.Context,
    prompt: str,
    model: str,
    max_completion_tokens: int | None,
    system: str | None,
    output_json: bool,
) -> None:
    """Send PROMPT through the unified Chat Completions API.

    \b
    Examples:
      aichat completions "Hello" -m kimi-k2.7-code
      aichat completions "Explain this" -m gemini-4-argon --json
    """
    if not model.strip():
        raise click.BadParameter("Model ID must not be empty.", param_hint="--model")
    client = get_client(ctx.obj.get("token"))
    conversation = []
    if system is not None:
        conversation.append({"role": "system", "content": system})
    conversation.append({"role": "user", "content": prompt})
    try:
        result = client.completions(
            model=model, messages=conversation, max_completion_tokens=max_completion_tokens
        )
        choices = result.get("choices") or []
        content = choices[0].get("message", {}).get("content") if choices else None
        if output_json or not isinstance(content, str):
            print_json(result)
        else:
            click.echo(content)
    except AichatError as exc:
        print_error(exc.message)
        raise SystemExit(1) from exc

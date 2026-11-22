"""Native Messages requests with an explicit, forward-compatible model ID."""

import click

from aichat_cli.core.client import get_client
from aichat_cli.core.exceptions import AichatError
from aichat_cli.core.output import print_error, print_json


@click.command()
@click.argument("prompt")
@click.option(
    "-m", "--model", required=True, help="Explicit model ID supporting the native Messages API."
)
@click.option("--max-tokens", type=click.IntRange(min=1), default=1024, show_default=True)
@click.option("-s", "--system", default=None, help="Optional system prompt.")
@click.option(
    "--json", "output_json", is_flag=True, help="Output the complete native JSON response."
)
@click.pass_context
def messages(
    ctx: click.Context,
    prompt: str,
    model: str,
    max_tokens: int,
    system: str | None,
    output_json: bool,
) -> None:
    """Send PROMPT through the native Messages API.

    Choose a model with a published Messages endpoint. IDs are passed through
    without a client-side model allowlist or fallback.

    \b
    Examples:
      aichat messages "Hello" -m claude-sonnet-5-5 --max-tokens 128
      aichat messages "Summarize this" -m claude-opus-5-5 --json
    """
    if not model.strip():
        raise click.BadParameter("Model ID must not be empty.", param_hint="--model")
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.messages(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            system=system,
        )
        content = result.get("content")
        text = (
            "".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            )
            if isinstance(content, list)
            else ""
        )
        if output_json or not text:
            print_json(result)
        else:
            click.echo(text)
    except AichatError as exc:
        print_error(exc.message)
        raise SystemExit(1) from exc

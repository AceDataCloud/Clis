"""Chat command."""

import click

from aichat_cli.core.client import get_client
from aichat_cli.core.exceptions import AichatError
from aichat_cli.core.output import DEFAULT_MODEL, MODELS, print_answer, print_error, print_json


@click.command()
@click.argument("question")
@click.option(
    "-m",
    "--model",
    default=DEFAULT_MODEL,
    type=click.Choice(MODELS, case_sensitive=True),
    help=f"Model to use (default: {DEFAULT_MODEL}).",
    show_default=True,
)
@click.option(
    "--id",
    "conversation_id",
    default=None,
    help="Conversation ID to continue an existing conversation.",
)
@click.option(
    "--preset",
    default=None,
    help="Preset model configuration to use.",
)
@click.option(
    "--stateful",
    is_flag=True,
    default=False,
    help="Enable stateful (multi-turn) conversation mode.",
)
@click.option(
    "-r",
    "--reference",
    "references",
    multiple=True,
    help="Reference URL or text to include (can be specified multiple times).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def chat(
    ctx: click.Context,
    question: str,
    model: str,
    conversation_id: str | None,
    preset: str | None,
    stateful: bool,
    references: tuple[str, ...],
    output_json: bool,
) -> None:
    """Send a question and get an AI-generated answer.

    QUESTION is the prompt or question to be answered.

    \b
    Examples:
      aichat chat "What is the capital of France?"
      aichat chat "Explain AI" -m gpt-4o
      aichat chat "Hello!" --stateful
      aichat chat "Continue our talk" --stateful --id <conversation-id>
      aichat chat "Summarize this" -r "https://example.com/article"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "question": question,
            "model": model,
            "id": conversation_id,
            "preset": preset,
            "stateful": stateful if stateful else None,
            "references": list(references) if references else None,
        }

        result = client.converse(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_answer(result)
    except AichatError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Chat command."""

import json as _json

import click

from aichat_cli.core.client import get_client
from aichat_cli.core.exceptions import AichatError
from aichat_cli.core.output import (
    ACTIONS2,
    DEFAULT_MODEL,
    DEFAULT_MODEL2,
    MODEL_GROUPS,
    MODELS,
    MODELS2,
    print_answer,
    print_error,
    print_json,
)


def _parse_json_option(value: str | None, param_hint: str) -> object:
    """Parse a JSON string option, raising BadParameter on invalid JSON."""
    if value is None:
        return None
    try:
        return _json.loads(value)
    except _json.JSONDecodeError as exc:
        raise click.BadParameter("Must be a valid JSON string.", param_hint=param_hint) from exc


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
    help="Preset model name.",
)
@click.option(
    "--stateful",
    is_flag=True,
    default=False,
    help="Enable stateful conversation (server remembers context).",
)
@click.option(
    "--ref",
    "references",
    multiple=True,
    help="Reference URL or text to include as context (can be repeated).",
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
    """Send a question to an AI model and get an answer.

    QUESTION is the prompt or question to send to the model.

    \b
    Examples:
      aichat chat "What is the capital of France?"
      aichat chat "Explain AI" -m gpt-4o
      aichat chat "Tell me more" --id 64a67fff-61dc-4801-8339-2c69334c61d6
      aichat chat "My name is Alice" --stateful
      aichat chat "Summarize this" --ref "https://example.com/doc.txt"
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


@click.command(name="chat2")
@click.argument("question")
@click.option(
    "-m",
    "--model",
    default=DEFAULT_MODEL2,
    type=click.Choice(MODELS2, case_sensitive=True),
    help=f"Model to use (default: {DEFAULT_MODEL2}).",
    show_default=True,
)
@click.option(
    "--action",
    default="chat",
    type=click.Choice(ACTIONS2),
    help="Action to perform (default: chat).",
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
    help="Preset model name.",
)
@click.option(
    "--stateful",
    is_flag=True,
    default=False,
    help="Enable stateful conversation (server remembers context).",
)
@click.option(
    "--ref",
    "references",
    multiple=True,
    help="Reference URL or text to include as context (can be repeated).",
)
@click.option(
    "--model-group",
    default=None,
    type=click.Choice(MODEL_GROUPS),
    help="Model group to use (e.g. chatgpt, claude, gemini).",
)
@click.option(
    "--max-turns",
    default=None,
    type=int,
    help="Maximum number of conversation turns.",
)
@click.option(
    "--title",
    default=None,
    help="Title for the conversation.",
)
@click.option(
    "--user-id",
    default=None,
    help="User ID for the conversation.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Callback URL for async results.",
)
@click.option(
    "--async-mode",
    "async_mode",
    is_flag=True,
    default=False,
    help="Enable asynchronous processing.",
)
@click.option(
    "--application-id",
    default=None,
    help="Application ID for the conversation.",
)
@click.option(
    "--allowed-skill",
    "allowed_skills",
    multiple=True,
    help="Allowed skill name (can be repeated).",
)
@click.option(
    "--allowed-mcp-server",
    "allowed_mcp_servers",
    multiple=True,
    help="Allowed MCP server name (can be repeated).",
)
@click.option(
    "--offset",
    default=None,
    type=int,
    help="Offset for paginated retrieval (minimum: 0).",
)
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Limit for paginated retrieval (1-100).",
)
@click.option(
    "--message",
    default=None,
    help="Single message value as a JSON string (alternative to --question for complex message types).",
)
@click.option(
    "--messages",
    default=None,
    help='Conversation messages as a JSON array, e.g. \'[{"role":"user","content":"Hello"}]\'.',
)
@click.option(
    "--tool-results",
    default=None,
    help='Tool call results as a JSON array, e.g. \'[{"tool_call_id":"id","content":"result"}]\'.',
)
@click.option(
    "--unattended-policy",
    default=None,
    help=(
        "Unattended agent policy as a JSON object, "
        'e.g. \'{"mode":"allow","allowed_skills":["web_search"]}\'.'
    ),
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def chat2(
    ctx: click.Context,
    question: str,
    model: str,
    action: str,
    conversation_id: str | None,
    preset: str | None,
    stateful: bool,
    references: tuple[str, ...],
    model_group: str | None,
    max_turns: int | None,
    title: str | None,
    user_id: str | None,
    callback_url: str | None,
    async_mode: bool,
    application_id: str | None,
    allowed_skills: tuple[str, ...],
    allowed_mcp_servers: tuple[str, ...],
    offset: int | None,
    limit: int | None,
    message: str | None,
    messages: str | None,
    tool_results: str | None,
    unattended_policy: str | None,
    output_json: bool,
) -> None:
    """Send a question to an AI model via the aichat2 endpoint.

    QUESTION is the prompt or question to send to the model.

    \b
    Examples:
      aichat chat2 "What is the capital of France?"
      aichat chat2 "Explain AI" -m claude-sonnet-5
      aichat chat2 "Tell me more" --id 64a67fff-61dc-4801-8339-2c69334c61d6
      aichat chat2 "Summarize this" --ref "https://example.com/doc.txt" --model-group claude
      aichat chat2 "Hello" --allowed-skill web_search --allowed-mcp-server my-server
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "question": question,
            "model": model,
            "action": action,
            "id": conversation_id,
            "preset": preset,
            "stateful": stateful if stateful else None,
            "references": list(references) if references else None,
            "model_group": model_group,
            "max_turns": max_turns,
            "title": title,
            "user_id": user_id,
            "application_id": application_id,
            "callback_url": callback_url,
            "async": async_mode if async_mode else None,
            "allowed_skills": list(allowed_skills) if allowed_skills else None,
            "allowed_mcp_servers": list(allowed_mcp_servers) if allowed_mcp_servers else None,
            "offset": offset,
            "limit": limit,
            "message": _parse_json_option(message, "--message"),
            "messages": _parse_json_option(messages, "--messages"),
            "tool_results": _parse_json_option(tool_results, "--tool-results"),
            "unattended_policy": _parse_json_option(unattended_policy, "--unattended-policy"),
        }

        result = client.converse2(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_answer(result)
    except AichatError as e:
        print_error(e.message)
        raise SystemExit(1) from e

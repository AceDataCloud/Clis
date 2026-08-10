"""Native Gemini generateContent commands."""

import click

from gemini_cli.commands._json import parse_json_array, parse_json_object
from gemini_cli.core.client import get_client
from gemini_cli.core.exceptions import GeminiError
from gemini_cli.core.output import GEMINI_NATIVE_MODELS, print_chat_result, print_error, print_json


def _build_payload(
    contents: str,
    system_instruction: str | None,
    generation_config: str | None,
    tools: str | None,
    tool_config: str | None,
    safety_settings: str | None,
) -> dict[str, object]:
    try:
        parsed_contents = parse_json_array(contents, "--contents")
        parsed_system_instruction = parse_json_object(system_instruction, "--system-instruction")
        parsed_generation_config = parse_json_object(generation_config, "--generation-config")
        parsed_tools = parse_json_array(tools, "--tools")
        parsed_tool_config = parse_json_object(tool_config, "--tool-config")
        parsed_safety_settings = parse_json_array(safety_settings, "--safety-settings")
    except click.BadParameter as e:
        print_error(e.format_message())
        raise SystemExit(1) from None

    return {
        "contents": parsed_contents,
        "systemInstruction": parsed_system_instruction,
        "generationConfig": parsed_generation_config,
        "tools": parsed_tools,
        "toolConfig": parsed_tool_config,
        "safetySettings": parsed_safety_settings,
    }


def _content_options(command):
    command = click.option("--safety-settings", default=None, help="Safety settings as a JSON array.")(
        command
    )
    command = click.option("--tool-config", default=None, help="Tool config as a JSON object.")(command)
    command = click.option("--tools", default=None, help="Tool definitions as a JSON array.")(command)
    command = click.option(
        "--generation-config",
        default=None,
        help="Generation config as a JSON object.",
    )(command)
    command = click.option(
        "--system-instruction",
        default=None,
        help="System instruction as a JSON object.",
    )(command)
    command = click.option(
        "--contents",
        required=True,
        help="Contents as a JSON array.",
    )(command)
    command = click.option(
        "-m",
        "--model",
        type=click.Choice(GEMINI_NATIVE_MODELS),
        required=True,
        help="Gemini model to use.",
    )(command)
    command = click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")(command)
    return command


@click.command("generate-content")
@_content_options
@click.pass_context
def generate_content(
    ctx: click.Context,
    output_json: bool,
    model: str,
    contents: str,
    system_instruction: str | None,
    generation_config: str | None,
    tools: str | None,
    tool_config: str | None,
    safety_settings: str | None,
) -> None:
    """Generate content using the native Gemini API."""
    client = get_client(ctx.obj.get("token"))
    payload = _build_payload(
        contents,
        system_instruction,
        generation_config,
        tools,
        tool_config,
        safety_settings,
    )

    try:
        result = client.generate_content(model, **payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_chat_result(result)
    except GeminiError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("stream-generate-content")
@_content_options
@click.option("--alt", type=click.Choice(["sse"]), default=None, help="Alternative stream format.")
@click.pass_context
def stream_generate_content(
    ctx: click.Context,
    alt: str | None,
    output_json: bool,
    model: str,
    contents: str,
    system_instruction: str | None,
    generation_config: str | None,
    tools: str | None,
    tool_config: str | None,
    safety_settings: str | None,
) -> None:
    """Stream content using the native Gemini API as server-sent events."""
    del output_json
    client = get_client(ctx.obj.get("token"))
    payload = _build_payload(
        contents,
        system_instruction,
        generation_config,
        tools,
        tool_config,
        safety_settings,
    )

    try:
        for event in client.stream_generate_content(model, alt=alt, **payload):  # type: ignore[arg-type]
            click.echo(event)
    except GeminiError as e:
        print_error(e.message)
        raise SystemExit(1) from e

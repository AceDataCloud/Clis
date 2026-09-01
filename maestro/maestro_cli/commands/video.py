"""Video creation commands."""

import click

from maestro_cli.core.client import get_client
from maestro_cli.core.exceptions import MaestroError
from maestro_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ACTION,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_DURATION,
    DEFAULT_SCENARIO,
    DEFAULT_STYLE,
    DEFAULT_VOICE,
    MAESTRO_ACTIONS,
    SCENARIOS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "--action",
    type=click.Choice(MAESTRO_ACTIONS),
    default=DEFAULT_ACTION,
    show_default=True,
    help="Action: generate = new video; remix/edit/extend = iterate on a previous video.",
)
@click.option(
    "--ref-task-id",
    default=None,
    help="Required when action is remix/edit/extend: task_id of the previous video.",
)
@click.option(
    "--file-url",
    "file_urls",
    multiple=True,
    help="Reference media URL(s) (image/video/audio). Can be specified multiple times.",
)
@click.option(
    "--lang",
    "langs",
    multiple=True,
    help=(
        "Output language(s) e.g. zh-cn, en. First is primary; each additional adds "
        "+6 credits. Defaults to zh-cn."
    ),
)
@click.option(
    "--aspect",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    show_default=True,
    help="Output aspect ratio.",
)
@click.option(
    "--duration",
    type=click.IntRange(5, 300),
    default=DEFAULT_DURATION,
    show_default=True,
    help="Target video length in seconds (5-300).",
)
@click.option(
    "--scenario",
    type=click.Choice(SCENARIOS),
    default=DEFAULT_SCENARIO,
    show_default=True,
    help="Production workflow: auto/narrated/captions/avatar/drama.",
)
@click.option(
    "--style",
    type=str,
    default=DEFAULT_STYLE,
    show_default=True,
    help="Visual-style preset or custom style hint.",
)
@click.option(
    "--voice",
    type=str,
    default=DEFAULT_VOICE,
    show_default=True,
    help="Narration voice timbre preset or a 32-char Fish reference_id.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def create(
    ctx: click.Context,
    prompt: str,
    action: str,
    ref_task_id: str | None,
    file_urls: tuple[str, ...],
    langs: tuple[str, ...],
    aspect: str,
    duration: int,
    scenario: str,
    style: str,
    voice: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Create a Maestro AI video from a prompt.

    PROMPT is a natural-language brief describing the video to produce.

    \b
    Examples:
      maestro create "Explain what a vector database is in 20 seconds"
      maestro create "Product demo" --aspect 16:9
      maestro create "Continue the story" --action extend --ref-task-id abc123
      maestro create "Same video in English" --action remix --ref-task-id abc123 --lang en
    """
    if action != "generate" and not ref_task_id:
        raise click.UsageError("--ref-task-id is required for remix, edit, and extend actions.")
    if len(file_urls) > 20:
        raise click.UsageError("At most 20 reference media URLs are allowed.")
    if len(langs) > 4:
        raise click.UsageError("At most 4 output languages are allowed.")

    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "prompt": prompt,
        "action": action,
        "aspect": aspect,
        "duration": duration,
        "scenario": scenario,
        "style": style,
        "voice": voice,
    }

    if ref_task_id:
        payload["ref_task_id"] = ref_task_id
    if file_urls:
        payload["file_urls"] = list(file_urls)
    if langs:
        payload["langs"] = list(langs)
    if callback_url:
        payload["callback_url"] = callback_url

    try:
        result = client.create_video(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except MaestroError as e:
        print_error(e.message)
        raise SystemExit(1) from e

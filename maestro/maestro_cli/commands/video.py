"""Video creation commands."""

import json
from pathlib import Path

import click

from maestro_cli.core.client import get_client
from maestro_cli.core.exceptions import MaestroError
from maestro_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ACTION,
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
    default=None,
    help="Output aspect ratio (new videos default to 9:16; edits inherit).",
)
@click.option(
    "--duration",
    type=click.IntRange(5, 300),
    default=None,
    help="Target length in seconds, 5-300 (new videos default to 30; edits inherit).",
)
@click.option(
    "--scenario",
    type=click.Choice(SCENARIOS),
    default=None,
    help="Production workflow: auto/narrated/captions/avatar/drama.",
)
@click.option(
    "--style",
    type=str,
    default=None,
    help="Visual style, including apple-launch, or a custom hint (edits inherit).",
)
@click.option(
    "--voice",
    type=str,
    default=None,
    help="Narration voice timbre preset or a 32-char Fish reference_id.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--audio-mode",
    type=click.Choice(["auto", "narration", "music", "silent"]),
    default=None,
    help="Audio intent; music has no narration. Omit to inherit on edit.",
)
@click.option(
    "--website-url", default=None, help="Public website source. An empty string clears it on edit."
)
@click.option(
    "--assets-file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="JSON array of role-labeled assets; [] clears them on edit.",
)
@click.option(
    "--brand-file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="JSON brand overrides; null clears them on edit.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def create(
    ctx: click.Context,
    prompt: str,
    action: str,
    ref_task_id: str | None,
    file_urls: tuple[str, ...],
    langs: tuple[str, ...],
    aspect: str | None,
    duration: int | None,
    scenario: str | None,
    style: str | None,
    voice: str | None,
    callback_url: str | None,
    audio_mode: str | None,
    website_url: str | None,
    assets_file: str | None,
    brand_file: str | None,
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
    }
    for key, value in {
        "aspect": aspect,
        "duration": duration,
        "scenario": scenario,
        "style": style,
        "voice": voice,
        "audio_mode": audio_mode,
    }.items():
        if value is not None:
            payload[key] = value
    if website_url is not None:
        payload["website_url"] = website_url or None
    for field, path in (("assets", assets_file), ("brand", brand_file)):
        if path is None:
            continue
        try:
            value = json.loads(Path(path).read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise click.UsageError(f"Cannot read {field} JSON: {exc}") from exc
        if field == "assets" and (not isinstance(value, list) or len(value) + len(file_urls) > 20):
            raise click.UsageError(
                "assets must be an array; assets and file URLs support at most 20 combined items."
            )
        if field == "brand" and value is not None and not isinstance(value, dict):
            raise click.UsageError("brand must be a JSON object or null.")
        payload[field] = value
    if audio_mode in {"music", "silent"} and voice not in (None, "auto"):
        raise click.UsageError("music/silent modes cannot pin a narration voice.")

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

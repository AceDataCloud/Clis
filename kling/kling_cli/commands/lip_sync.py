"""Lip-sync generation command."""

from typing import Any

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import print_error, print_json, print_video_result

LIP_SYNC_MODES = ["audio2video", "text2video"]
LIP_SYNC_AUDIO_TYPES = ["url", "file"]


@click.command("lip-sync")
@click.option(
    "--mode",
    required=True,
    type=click.Choice(LIP_SYNC_MODES),
    help="Lip-sync mode: audio2video (drive with audio) or text2video (drive with text + voice).",
)
@click.option("--video-id", default=None, help="ID of the Kling-generated video to lip-sync.")
@click.option("--video-url", default=None, help="Public URL of the 5s/10s video to lip-sync.")
@click.option(
    "--audio-url",
    default=None,
    help="Public URL of the driving audio (required for audio2video).",
)
@click.option(
    "--audio-type",
    type=click.Choice(LIP_SYNC_AUDIO_TYPES),
    default=None,
    help="How the audio is supplied for audio2video.",
)
@click.option(
    "--text",
    default=None,
    help="Text to speak (required for text2video; max 120 characters).",
)
@click.option("--voice-id", default=None, help="Voice ID to use for text2video.")
@click.option(
    "--voice-language",
    default=None,
    help="Voice language for text2video (defaults to zh).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def lip_sync(
    ctx: click.Context,
    mode: str,
    video_id: str | None,
    video_url: str | None,
    audio_url: str | None,
    audio_type: str | None,
    text: str | None,
    voice_id: str | None,
    voice_language: str | None,
    callback_url: str | None,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Drive an existing Kling video with audio or text so the character speaks in sync."""
    if not video_id and not video_url:
        raise click.UsageError("Provide --video-id or --video-url.")
    if mode == "audio2video" and not audio_url:
        raise click.UsageError("Provide --audio-url when --mode audio2video is used.")
    if mode == "text2video":
        if not text:
            raise click.UsageError("Provide --text when --mode text2video is used.")
        if len(text) > 120:
            raise click.UsageError("--text must be 120 characters or fewer.")
        if not voice_id:
            raise click.UsageError("Provide --voice-id when --mode text2video is used.")

    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, Any] = {
            "mode": mode,
            "video_id": video_id,
            "video_url": video_url,
            "audio_url": audio_url,
            "audio_type": audio_type,
            "text": text,
            "voice_id": voice_id,
            "voice_language": voice_language,
            "callback_url": callback_url,
        }
        result = client.generate_lip_sync(timeout=timeout, **payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

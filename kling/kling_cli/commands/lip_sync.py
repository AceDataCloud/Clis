"""Lip sync generation command."""

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import print_error, print_json, print_video_result

LIP_SYNC_MODES = ["audio2video", "text2video"]
VOICE_LANGUAGES = ["zh", "en"]


def _validate_lip_sync_inputs(
    mode: str,
    video_id: str | None,
    video_url: str | None,
    audio_url: str | None,
    audio_file: str | None,
    text: str | None,
    voice_id: str | None,
    voice_speed: float | None,
) -> None:
    """Validate lip-sync inputs against the API contract."""
    if bool(video_id) == bool(video_url):
        raise click.UsageError("Provide exactly one of --video-id or --video-url.")

    if mode == "audio2video":
        if bool(audio_url) == bool(audio_file):
            raise click.UsageError("Provide exactly one of --audio-url or --audio-file.")
        return

    if not text:
        raise click.UsageError("Provide --text when --mode text2video.")
    if len(text) > 120:
        raise click.BadParameter("Text must be at most 120 characters.", param_hint="--text")
    if not voice_id:
        raise click.UsageError("Provide --voice-id when --mode text2video.")
    if voice_speed is not None and not 0.8 <= voice_speed <= 2.0:
        raise click.BadParameter(
            "Voice speed must be between 0.8 and 2.0.",
            param_hint="--voice-speed",
        )


@click.command("lip-sync")
@click.option(
    "--mode",
    required=True,
    type=click.Choice(LIP_SYNC_MODES),
    help="Lip-sync mode: audio2video or text2video.",
)
@click.option("--video-id", default=None, help="ID of an existing Kling video to drive.")
@click.option("--video-url", default=None, help="Public URL of a video to drive.")
@click.option(
    "--audio-url",
    default=None,
    help="Download URL of the driving audio (used with --mode audio2video).",
)
@click.option(
    "--audio-file",
    default=None,
    help="Base64-encoded audio content (used with --mode audio2video).",
)
@click.option(
    "--text",
    default=None,
    help="Text to speak (used with --mode text2video, max 120 characters).",
)
@click.option(
    "--voice-id",
    default=None,
    help="Voice ID to use for text-to-video lip sync.",
)
@click.option(
    "--voice-language",
    type=click.Choice(VOICE_LANGUAGES),
    default="zh",
    show_default=True,
    help="Voice language for text-to-video lip sync.",
)
@click.option(
    "--voice-speed",
    type=float,
    default=None,
    help="Voice speed for text-to-video lip sync (0.8 to 2.0).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def lip_sync(
    ctx: click.Context,
    mode: str,
    video_id: str | None,
    video_url: str | None,
    audio_url: str | None,
    audio_file: str | None,
    text: str | None,
    voice_id: str | None,
    voice_language: str,
    voice_speed: float | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Drive an existing video with audio or text for synchronized speech.

    Examples:

      kling lip-sync --mode audio2video --video-id 895055164389466178 --audio-url https://example.com/voice.mp3

      kling lip-sync --mode text2video --video-id 895055164389466178 --text "Hello there" --voice-id genshin_vindi2 --voice-language en
    """
    _validate_lip_sync_inputs(
        mode=mode,
        video_id=video_id,
        video_url=video_url,
        audio_url=audio_url,
        audio_file=audio_file,
        text=text,
        voice_id=voice_id,
        voice_speed=voice_speed,
    )

    client = get_client(ctx.obj.get("token"))
    try:
        audio_type = None
        if mode == "audio2video":
            audio_type = "file" if audio_file else "url"

        payload = {
            "mode": mode,
            "video_id": video_id,
            "video_url": video_url,
            "audio_url": audio_url if mode == "audio2video" else None,
            "audio_type": audio_type,
            "audio_file": audio_file if mode == "audio2video" else None,
            "text": text if mode == "text2video" else None,
            "voice_id": voice_id if mode == "text2video" else None,
            "voice_language": voice_language if mode == "text2video" else None,
            "voice_speed": voice_speed if mode == "text2video" else None,
            "callback_url": callback_url,
            "async": async_mode,
        }
        result = client.generate_lip_sync(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

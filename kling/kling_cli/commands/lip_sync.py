"""Lip-sync command."""

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import print_error, print_json, print_video_result


@click.command("lip-sync")
@click.option(
    "--mode",
    required=True,
    type=click.Choice(["audio2video", "text2video"]),
    help="Driving mode: audio2video (drive with an audio clip) or text2video (drive with text + a voice).",
)
@click.option("--video-id", default=None, help="ID of a Kling-generated video to lip-sync.")
@click.option("--video-url", default=None, help="Public URL of a 5s/10s video to lip-sync.")
@click.option(
    "--audio-url",
    default=None,
    help="Public URL of the driving audio (required when mode is audio2video and audio-type is url).",
)
@click.option(
    "--audio-type",
    default=None,
    type=click.Choice(["url", "file"]),
    help="How the audio is supplied for audio2video mode.",
)
@click.option(
    "--audio-file",
    default=None,
    help="Base64-encoded audio file content (required when audio-type is file). Supports .mp3/.wav/.m4a/.aac.",
)
@click.option(
    "--text",
    default=None,
    help="Text to speak (required when mode is text2video, max 120 chars).",
)
@click.option(
    "--voice-id",
    default=None,
    help="Voice ID to use (required when mode is text2video).",
)
@click.option(
    "--voice-language",
    default=None,
    type=click.Choice(["zh", "en"]),
    help="Voice language for text2video mode.",
)
@click.option(
    "--voice-speed",
    default=None,
    type=float,
    help="Speech rate for text2video (0.8-2.0, one decimal place).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Return a task_id immediately and poll via 'task' command.",
)
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
    audio_file: str | None,
    text: str | None,
    voice_id: str | None,
    voice_language: str | None,
    voice_speed: float | None,
    callback_url: str | None,
    async_mode: bool,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Lip-sync a video using audio or text-to-speech.

    Provide either --video-id (for a Kling-generated video) or --video-url.

    \b
    Audio2video examples:
      kling lip-sync --mode audio2video --video-id abc123 --audio-url https://example.com/audio.mp3

    \b
    Text2video examples:
      kling lip-sync --mode text2video --video-url https://example.com/video.mp4 \\
        --text "Hello world" --voice-id en-US-1 --voice-language en
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "mode": mode,
            "video_id": video_id,
            "video_url": video_url,
            "audio_url": audio_url,
            "audio_type": audio_type,
            "audio_file": audio_file,
            "text": text,
            "voice_id": voice_id,
            "voice_language": voice_language,
            "voice_speed": voice_speed,
            "callback_url": callback_url,
            "async": async_mode if async_mode else None,
            "timeout": timeout,
        }
        result = client.generate_lip_sync(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Creative generation commands (lip-sync, talking-photo)."""

import click

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import (
    DEFAULT_MODE,
    print_error,
    print_json,
    print_video_result,
)

TALKING_PHOTO_MODELS = [
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
]
DEFAULT_TALKING_PHOTO_MODEL = "kling-v2-1-master"

TALKING_PHOTO_MODES = ["std", "pro"]

LIP_SYNC_MODES = ["audio2video", "text2video"]


@click.command("lip-sync")
@click.option(
    "--mode",
    required=True,
    type=click.Choice(LIP_SYNC_MODES),
    help="Lip sync mode: audio2video (drive by audio) or text2video (drive by text/TTS).",
)
@click.option("--video-id", default=None, help="ID of the video to apply lip sync to.")
@click.option("--video-url", default=None, help="URL of the video to apply lip sync to.")
@click.option(
    "--audio-url",
    default=None,
    help="URL of the audio file (required for audio2video mode).",
)
@click.option(
    "--audio-type",
    default=None,
    type=click.Choice(["url", "file"]),
    help="Audio source type (default: url).",
)
@click.option(
    "--audio-file",
    default=None,
    help="Audio file content (used when --audio-type is file).",
)
@click.option(
    "--text",
    default=None,
    help="Text to synthesize as speech (required for text2video mode, max 120 characters).",
)
@click.option("--voice-id", default=None, help="Voice ID for TTS synthesis.")
@click.option(
    "--voice-language",
    default=None,
    type=click.Choice(["zh", "en"]),
    help="Voice language for TTS (default: zh).",
)
@click.option(
    "--voice-speed",
    default=None,
    type=float,
    help="Voice speed for TTS, between 0.8 and 2.0 (default: 1.0).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
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
    """Apply lip sync to a video using audio or text-to-speech.

    Use --mode audio2video to drive lip sync with an audio file, or --mode text2video
    to generate speech from text and synchronize it to the video.

    Examples:

      kling lip-sync --mode audio2video --video-url https://example.com/video.mp4 --audio-url https://example.com/audio.mp3

      kling lip-sync --mode text2video --video-id abc123 --text "Hello world" --voice-language en
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.lip_sync(
            mode=mode,
            video_id=video_id,
            video_url=video_url,
            audio_url=audio_url,
            audio_type=audio_type,
            audio_file=audio_file,
            text=text,
            voice_id=voice_id,
            voice_language=voice_language,
            voice_speed=voice_speed,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
            timeout=timeout,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("talking-photo")
@click.option(
    "--image-url",
    required=True,
    help="URL of the photo to animate.",
)
@click.option(
    "--audio-url",
    required=True,
    help="URL of the audio file to synchronize with the photo.",
)
@click.option("--prompt", default=None, help="Optional text prompt to guide generation.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(TALKING_PHOTO_MODELS),
    default=DEFAULT_TALKING_PHOTO_MODEL,
    help="Model to use for generation.",
)
@click.option(
    "--duration",
    default=None,
    type=click.Choice(["5", "10"]),
    help="Video duration in seconds (5 or 10, default: 5).",
)
@click.option(
    "--mode",
    type=click.Choice(TALKING_PHOTO_MODES),
    default=DEFAULT_MODE,
    help="Generation mode: std (High performance) or pro (High quality).",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option(
    "--timeout", default=None, type=int, help="Timeout in seconds for the API to return data."
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def talking_photo(
    ctx: click.Context,
    image_url: str,
    audio_url: str,
    prompt: str | None,
    model: str,
    duration: str | None,
    mode: str,
    callback_url: str | None,
    async_mode: bool,
    timeout: int | None,
    output_json: bool,
) -> None:
    """Animate a photo with synchronized audio (talking photo).

    Generates a video of a photo speaking in sync with the provided audio.

    Examples:

      kling talking-photo --image-url https://example.com/photo.jpg --audio-url https://example.com/speech.mp3

      kling talking-photo --image-url photo.jpg --audio-url speech.mp3 --model kling-v2-6 --duration 10
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.talking_photo(
            image_url=image_url,
            audio_url=audio_url,
            prompt=prompt,
            model=model,
            duration=int(duration) if duration else None,
            mode=mode,
            callback_url=callback_url,
            **({"async": True} if async_mode else {}),
            timeout=timeout,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except KlingError as e:
        print_error(e.message)
        raise SystemExit(1) from e

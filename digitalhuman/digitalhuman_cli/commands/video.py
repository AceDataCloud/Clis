"""Video generation commands for Digital Human CLI."""

import click

from digitalhuman_cli.core.client import get_client
from digitalhuman_cli.core.exceptions import DigitalHumanError
from digitalhuman_cli.core.output import (
    DEFAULT_ENGINE,
    DEFAULT_RESOLUTION,
    ENGINES,
    RESOLUTIONS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.option(
    "--video-url",
    default=None,
    help="Public URL of the source face video (preferred).",
)
@click.option(
    "--image-url",
    default=None,
    help="Public URL of a source face photo (photo-driven path).",
)
@click.option(
    "--audio-url",
    default=None,
    help="Public URL of the driving audio (.wav/.mp3/.m4a).",
)
@click.option(
    "--text",
    default=None,
    help="Spoken text for TTS (requires --voice-id).",
)
@click.option(
    "--voice-id",
    default=None,
    help="Cloned voice ID from 'digitalhuman clone-voice'.",
)
@click.option(
    "--engine",
    type=click.Choice(ENGINES),
    default=DEFAULT_ENGINE,
    show_default=True,
    help="Engine to use: latentsync (quality) or heygem (fast).",
)
@click.option(
    "--guidance",
    type=float,
    default=None,
    help="Lip-sync strength for LatentSync (default: 2.0). Lower loosens sync.",
)
@click.option(
    "--steps",
    type=int,
    default=None,
    help="Diffusion steps for LatentSync (default: 40).",
)
@click.option(
    "--no-seam-fix",
    "seam_fix",
    is_flag=True,
    default=False,
    help="Disable mouth-seam reduction blend (default: enabled).",
)
@click.option(
    "--speed",
    type=float,
    default=None,
    help="Audio tempo multiplier (default: 1.0).",
)
@click.option(
    "--resolution",
    type=click.Choice(RESOLUTIONS),
    default=DEFAULT_RESOLUTION,
    show_default=True,
    help="Output video resolution.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Webhook callback URL.",
)
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    video_url: str | None,
    image_url: str | None,
    audio_url: str | None,
    text: str | None,
    voice_id: str | None,
    engine: str,
    guidance: float | None,
    steps: int | None,
    seam_fix: bool,
    speed: float | None,
    resolution: str,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a digital human video.

    Requires either --video-url or --image-url as the face source.
    Audio can be provided via --audio-url or generated via --text + --voice-id.

    \b
    Examples:
      digitalhuman generate --video-url https://example.com/face.mp4 \\
                            --audio-url https://example.com/speech.mp3
      digitalhuman generate --image-url https://example.com/portrait.jpg \\
                            --audio-url https://example.com/speech.mp3 --async
      digitalhuman generate --video-url https://example.com/face.mp4 \\
                            --text "Hello world" --voice-id f754a190e26c
    """
    if not video_url and not image_url:
        raise click.UsageError("Provide either --video-url or --image-url.")
    if not audio_url and not text:
        raise click.UsageError("Provide either --audio-url or --text (with --voice-id).")
    if text and not voice_id:
        raise click.UsageError("--text requires --voice-id.")

    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "engine": engine,
        "resolution": resolution,
    }
    if video_url:
        payload["video_url"] = video_url
    if image_url:
        payload["image_url"] = image_url
    if audio_url:
        payload["audio_url"] = audio_url
    if text:
        payload["text"] = text
    if voice_id:
        payload["voice_id"] = voice_id
    if guidance is not None:
        payload["guidance"] = guidance
    if steps is not None:
        payload["steps"] = steps
    if seam_fix:
        payload["seam_fix"] = False
    if speed is not None:
        payload["speed"] = speed
    if callback_url:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate_video(**payload)
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except DigitalHumanError as e:
        print_error(e.message)
        raise SystemExit(1) from e

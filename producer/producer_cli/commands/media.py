"""Media commands for upload, video, and WAV generation."""

import click

from producer_cli.core.client import get_client
from producer_cli.core.exceptions import ProducerError
from producer_cli.core.output import (
    print_audio_result,
    print_error,
    print_json,
    print_media_result,
    print_upload_result,
)


@click.command()
@click.argument("audio_url")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upload(
    ctx: click.Context,
    audio_url: str,
    output_json: bool,
) -> None:
    """Upload an audio file from a URL.

    AUDIO_URL is the URL of the audio file to upload.

    \b
    Examples:
      producer upload https://example.com/my-audio.mp3
      producer upload https://cdn.example.com/song.wav
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.upload_audio(audio_url=audio_url)
        if output_json:
            print_json(result)
        else:
            print_upload_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def video(
    ctx: click.Context,
    audio_id: str,
    output_json: bool,
) -> None:
    """Generate a video for an existing audio track.

    AUDIO_ID is the ID of the audio track to generate a video for.

    \b
    Examples:
      producer video abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(audio_id=audio_id)
        if output_json:
            print_json(result)
        else:
            print_media_result(result, title="Video Result")
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def wav(
    ctx: click.Context,
    audio_id: str,
    output_json: bool,
) -> None:
    """Get the WAV format of an existing audio track.

    AUDIO_ID is the ID of the audio track to convert to WAV.

    \b
    Examples:
      producer wav abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_wav(audio_id=audio_id)
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e

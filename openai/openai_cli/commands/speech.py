"""Audio speech synthesis command."""

from pathlib import Path

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import print_error, print_json, print_success

SPEECH_MODELS = ["tts-1", "tts-1-hd"]
SPEECH_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
SPEECH_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]


def _default_output_path(output: str | None, response_format: str) -> Path:
    """Resolve the output path for synthesized audio."""
    if output:
        return Path(output)
    return Path(f"speech.{response_format}")


@click.command()
@click.argument("input_text")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SPEECH_MODELS),
    default="tts-1-hd",
    show_default=True,
    help="Speech synthesis model to use.",
)
@click.option(
    "--voice",
    type=click.Choice(SPEECH_VOICES),
    default="alloy",
    show_default=True,
    help="Voice preset for the synthesized speech.",
)
@click.option(
    "--response-format",
    type=click.Choice(SPEECH_FORMATS),
    default="mp3",
    show_default=True,
    help="Audio container/codec to save.",
)
@click.option(
    "--speed",
    type=float,
    default=None,
    help="Playback speed multiplier.",
)
@click.option(
    "-o",
    "--output",
    default=None,
    help="Destination file path. Defaults to speech.<response-format> in the current directory.",
)
@click.option("--json", "output_json", is_flag=True, help="Output save metadata as JSON.")
@click.pass_context
def speech(
    ctx: click.Context,
    input_text: str,
    model: str,
    voice: str,
    response_format: str,
    speed: float | None,
    output: str | None,
    output_json: bool,
) -> None:
    """Synthesize speech audio from text using `/v1/audio/speech`."""
    client = get_client(ctx.obj.get("token"))
    output_path = _default_output_path(output, response_format)

    payload: dict[str, object] = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": response_format,
        "speed": speed,
    }

    try:
        audio_bytes = client.audio_speech(**payload)
        output_path.write_bytes(audio_bytes)

        result = {
            "path": str(output_path),
            "bytes": len(audio_bytes),
            "model": model,
            "voice": voice,
            "response_format": response_format,
        }
        if output_json:
            print_json(result)
        else:
            print_success(f"Saved synthesized audio to {output_path}")
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

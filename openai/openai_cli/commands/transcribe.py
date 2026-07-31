"""Audio transcription command."""

from pathlib import Path

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import print_error, print_json, print_transcription_result

TRANSCRIPTION_MODELS = ["whisper-1"]
TRANSCRIPTION_FORMATS = ["json", "text", "srt", "verbose_json", "vtt"]


@click.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-m",
    "--model",
    type=click.Choice(TRANSCRIPTION_MODELS),
    default="whisper-1",
    show_default=True,
    help="Transcription model to use.",
)
@click.option(
    "--language",
    default=None,
    help="Language of the input audio (ISO-639-1 code, e.g. 'en').",
)
@click.option(
    "--prompt",
    default=None,
    help="Optional text to guide the model's style or continue a previous segment.",
)
@click.option(
    "--response-format",
    type=click.Choice(TRANSCRIPTION_FORMATS),
    default="json",
    show_default=True,
    help="Format of the transcription output.",
)
@click.option(
    "--temperature",
    default=None,
    type=float,
    help="Sampling temperature (0-1). Higher values = more random.",
)
@click.option(
    "--timestamp-granularities",
    "timestamp_granularities",
    multiple=True,
    type=click.Choice(["word", "segment"]),
    help="Timestamp granularities to include (repeatable: word, segment).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def transcribe(
    ctx: click.Context,
    file: str,
    model: str,
    language: str | None,
    prompt: str | None,
    response_format: str,
    temperature: float | None,
    timestamp_granularities: tuple[str, ...],
    output_json: bool,
) -> None:
    """Transcribe audio to text using `/v1/audio/transcriptions`.

    FILE is the path to the audio file to transcribe.

    \b
    Examples:
      openai-cli transcribe audio.mp3
      openai-cli transcribe audio.wav --language en --response-format text
      openai-cli transcribe audio.mp3 --timestamp-granularities word
    """
    client = get_client(ctx.obj.get("token"))
    file_path = Path(file)
    audio_bytes = file_path.read_bytes()

    kwargs: dict[str, object] = {
        "model": model,
        "language": language,
        "prompt": prompt,
        "response_format": response_format,
        "temperature": temperature,
        "timestamp_granularities": list(timestamp_granularities) if timestamp_granularities else None,
    }

    try:
        result = client.audio_transcriptions(
            file=audio_bytes,
            filename=file_path.name,
            **kwargs,  # type: ignore[arg-type]
        )
        if output_json:
            print_json(result)
        else:
            print_transcription_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e

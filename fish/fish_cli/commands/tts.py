"""Text-to-speech command."""

import click

from fish_cli.core.client import get_client
from fish_cli.core.exceptions import FishError
from fish_cli.core.output import (
    DEFAULT_AUDIO_FORMAT,
    DEFAULT_LATENCY_MODE,
    DEFAULT_TTS_MODEL,
    FISH_AUDIO_FORMATS,
    FISH_LATENCY_MODES,
    FISH_MP3_BITRATES,
    FISH_TTS_MODELS,
    print_error,
    print_json,
    print_tts_result,
)


@click.command()
@click.argument("text")
@click.option(
    "-m",
    "--model",
    type=click.Choice(FISH_TTS_MODELS),
    default=DEFAULT_TTS_MODEL,
    help="TTS model to use.",
)
@click.option(
    "--reference-id",
    default=None,
    help="Voice model ID for single-speaker synthesis.",
)
@click.option(
    "--format",
    "audio_format",
    type=click.Choice(FISH_AUDIO_FORMATS),
    default=DEFAULT_AUDIO_FORMAT,
    help="Output audio format.",
)
@click.option(
    "--sample-rate",
    type=int,
    default=None,
    help="Sampling rate of the output audio (e.g. 16000, 22050, 44100).",
)
@click.option(
    "--mp3-bitrate",
    type=click.Choice([str(b) for b in FISH_MP3_BITRATES]),
    default=None,
    help="MP3 bit rate when --format=mp3.",
)
@click.option(
    "--opus-bitrate",
    type=int,
    default=None,
    help="Opus bit rate when --format=opus.",
)
@click.option(
    "--latency",
    type=click.Choice(FISH_LATENCY_MODES),
    default=DEFAULT_LATENCY_MODE,
    help="Latency mode.",
)
@click.option(
    "--chunk-length",
    type=int,
    default=None,
    help="Chunk length passed to the upstream synthesiser.",
)
@click.option(
    "--min-chunk-length",
    type=int,
    default=None,
    help="Minimum chunk length.",
)
@click.option(
    "--temperature",
    type=float,
    default=None,
    help="Sampling temperature (0.0–1.0).",
)
@click.option(
    "--top-p",
    type=float,
    default=None,
    help="Top-p nucleus sampling parameter.",
)
@click.option(
    "--repetition-penalty",
    type=float,
    default=None,
    help="Repetition penalty applied during generation.",
)
@click.option(
    "--max-new-tokens",
    type=int,
    default=None,
    help="Maximum number of new tokens to generate.",
)
@click.option(
    "--normalize/--no-normalize",
    default=None,
    help="Whether the upstream should apply text normalization.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Webhook callback URL. When set, synthesis runs asynchronously and returns a task ID.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def tts(
    ctx: click.Context,
    text: str,
    model: str,
    reference_id: str | None,
    audio_format: str,
    sample_rate: int | None,
    mp3_bitrate: str | None,
    opus_bitrate: int | None,
    latency: str,
    chunk_length: int | None,
    min_chunk_length: int | None,
    temperature: float | None,
    top_p: float | None,
    repetition_penalty: float | None,
    max_new_tokens: int | None,
    normalize: bool | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Synthesize TEXT to speech using Fish AI.

    TEXT is the text string to convert to audio.

    Examples:

      fish tts "Hello, world!"

      fish tts "Hello" --reference-id <voice-id> --format wav

      fish tts "Hello" --model s1 --latency balanced --json
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.synthesize(
            model=model,
            text=text,
            reference_id=reference_id,
            format=audio_format,
            sample_rate=sample_rate,
            mp3_bitrate=int(mp3_bitrate) if mp3_bitrate is not None else None,
            opus_bitrate=opus_bitrate,
            latency=latency,
            chunk_length=chunk_length,
            min_chunk_length=min_chunk_length,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_tokens,
            normalize=normalize,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_tts_result(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e

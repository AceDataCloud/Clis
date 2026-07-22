"""TTS generation command."""

import json

import click

from fish_cli.core.client import get_client
from fish_cli.core.exceptions import FishError
from fish_cli.core.output import (
    AUDIO_FORMATS,
    DEFAULT_AUDIO_FORMAT,
    DEFAULT_LATENCY,
    DEFAULT_TTS_MODEL,
    FISH_TTS_MODELS,
    LATENCY_MODES,
    print_error,
    print_json,
    print_tts_result,
)


def _parse_json_object_option(value: str | None, option_name: str) -> dict[str, object] | None:
    """Parse a JSON object option."""
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be valid JSON.") from exc
    if not isinstance(parsed, dict):
        raise click.BadParameter(f"{option_name} must be a JSON object.")
    return parsed


def _parse_json_array_option(value: str | None, option_name: str) -> list[object] | None:
    """Parse a JSON array option."""
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be valid JSON.") from exc
    if not isinstance(parsed, list):
        raise click.BadParameter(f"{option_name} must be a JSON array.")
    return parsed


@click.command()
@click.argument("text")
@click.option(
    "-m",
    "--model",
    type=click.Choice(FISH_TTS_MODELS),
    default=DEFAULT_TTS_MODEL,
    show_default=True,
    help="Fish TTS model to use (passed as HTTP header).",
)
@click.option(
    "--reference-id",
    default=None,
    help="Reference voice model ID for cloned voice.",
)
@click.option(
    "--format",
    "audio_format",
    type=click.Choice(AUDIO_FORMATS),
    default=DEFAULT_AUDIO_FORMAT,
    show_default=True,
    help="Output audio format.",
)
@click.option(
    "--sample-rate",
    type=int,
    default=None,
    help="Output sample rate in Hz.",
)
@click.option(
    "--mp3-bitrate",
    type=int,
    default=None,
    help="MP3 output bitrate.",
)
@click.option(
    "--opus-bitrate",
    type=int,
    default=None,
    help="Opus output bitrate.",
)
@click.option(
    "--latency",
    type=click.Choice(LATENCY_MODES),
    default=DEFAULT_LATENCY,
    show_default=True,
    help="Latency mode.",
)
@click.option(
    "--chunk-length",
    type=int,
    default=None,
    help="Streaming chunk length.",
)
@click.option(
    "--min-chunk-length",
    type=int,
    default=None,
    help="Minimum streaming chunk length.",
)
@click.option(
    "--temperature",
    type=float,
    default=None,
    help="Sampling temperature.",
)
@click.option(
    "--top-p",
    type=float,
    default=None,
    help="Top-p sampling parameter.",
)
@click.option(
    "--repetition-penalty",
    type=float,
    default=None,
    help="Repetition penalty.",
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
    help="Normalize audio output.",
)
@click.option(
    "--prosody",
    default=None,
    help="Prosody controls as a JSON object.",
)
@click.option(
    "--references",
    default=None,
    help="Reference clips as a JSON array.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Webhook callback URL for async delivery.",
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
def tts(
    ctx: click.Context,
    text: str,
    model: str,
    reference_id: str | None,
    audio_format: str,
    sample_rate: int | None,
    mp3_bitrate: int | None,
    opus_bitrate: int | None,
    latency: str,
    chunk_length: int | None,
    min_chunk_length: int | None,
    temperature: float | None,
    top_p: float | None,
    repetition_penalty: float | None,
    max_new_tokens: int | None,
    normalize: bool | None,
    prosody: str | None,
    references: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate text-to-speech audio using Fish Audio.

    TEXT is the text to convert to speech.

    \\b
    Examples:
      fish tts "Hello, world!"
      fish tts "Hello" --reference-id d7900c21663f485ab63ebdb7e5905036
      fish tts "Hello" --format wav --latency balanced --async
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "text": text,
        "format": audio_format,
        "latency": latency,
    }
    if reference_id is not None:
        payload["reference_id"] = reference_id
    if sample_rate is not None:
        payload["sample_rate"] = sample_rate
    if mp3_bitrate is not None:
        payload["mp3_bitrate"] = mp3_bitrate
    if opus_bitrate is not None:
        payload["opus_bitrate"] = opus_bitrate
    if chunk_length is not None:
        payload["chunk_length"] = chunk_length
    if min_chunk_length is not None:
        payload["min_chunk_length"] = min_chunk_length
    if temperature is not None:
        payload["temperature"] = temperature
    if top_p is not None:
        payload["top_p"] = top_p
    if repetition_penalty is not None:
        payload["repetition_penalty"] = repetition_penalty
    if max_new_tokens is not None:
        payload["max_new_tokens"] = max_new_tokens
    if normalize is not None:
        payload["normalize"] = normalize
    parsed_prosody = _parse_json_object_option(prosody, "--prosody")
    if parsed_prosody is not None:
        payload["prosody"] = parsed_prosody
    parsed_references = _parse_json_array_option(references, "--references")
    if parsed_references is not None:
        payload["references"] = parsed_references
    if callback_url is not None:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True

    try:
        result = client.generate_tts(model=model, **payload)
        if output_json:
            print_json(result)
        else:
            print_tts_result(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e

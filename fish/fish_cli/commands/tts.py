"""TTS generation command."""

import json
from urllib.parse import urlparse

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
    """Parse and validate a one-shot reference array."""
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be valid JSON.") from exc
    if not isinstance(parsed, list):
        raise click.BadParameter(f"{option_name} must be a JSON array.")
    if len(parsed) != 1 or not isinstance(parsed[0], dict):
        raise click.BadParameter(f"{option_name} must contain exactly one object.")
    reference = parsed[0]
    if set(reference) != {"audio", "text"}:
        raise click.BadParameter(f"{option_name} items must contain only audio and text.")
    _validate_reference_url(reference["audio"], option_name)
    if not isinstance(reference["text"], str) or not reference["text"].strip():
        raise click.BadParameter(f"{option_name} text must be non-empty.")
    return parsed


def _validate_reference_url(value: object, option_name: str) -> str:
    if not isinstance(value, str):
        raise click.BadParameter(f"{option_name} audio must be an HTTPS URL.")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise click.BadParameter(f"{option_name} audio must be an HTTPS URL without credentials.")
    return value


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
    multiple=True,
    help="Reference voice model ID for cloned voice; repeat to provide multiple IDs.",
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
    type=click.Choice(["64", "128", "192"]),
    default=None,
    help="MP3 output bitrate.",
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
    help='Advanced one-shot reference JSON: [{"audio":"https://...","text":"exact transcript"}].',
)
@click.option(
    "--reference-audio-url",
    default=None,
    help="Public HTTPS MP3/WAV URL for a one-shot voice clone.",
)
@click.option(
    "--reference-text",
    default=None,
    help="Exact transcript of --reference-audio-url.",
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
    reference_id: tuple[str, ...],
    audio_format: str,
    sample_rate: int | None,
    mp3_bitrate: str | None,
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
    reference_audio_url: str | None,
    reference_text: str | None,
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
      fish tts "Hello" --reference-audio-url https://cdn.example/ref.mp3 --reference-text "Exact transcript"
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "text": text,
        "format": audio_format,
        "latency": latency,
    }
    if reference_id:
        payload["reference_id"] = reference_id[0] if len(reference_id) == 1 else list(reference_id)
    if sample_rate is not None:
        payload["sample_rate"] = sample_rate
    if mp3_bitrate is not None:
        payload["mp3_bitrate"] = int(mp3_bitrate)
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
    if (reference_audio_url is None) != (reference_text is None):
        raise click.BadParameter(
            "--reference-audio-url and --reference-text must be provided together."
        )
    if parsed_references is not None and reference_audio_url is not None:
        raise click.BadParameter("Use --references or the convenience reference options, not both.")
    if reference_id and (parsed_references is not None or reference_audio_url is not None):
        raise click.BadParameter("--reference-id cannot be combined with one-shot references.")
    if reference_audio_url is not None and reference_text is not None:
        parsed_references = [
            {
                "audio": _validate_reference_url(reference_audio_url, "--reference-audio-url"),
                "text": reference_text.strip(),
            }
        ]
        if not parsed_references[0]["text"]:
            raise click.BadParameter("--reference-text must be non-empty.")
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

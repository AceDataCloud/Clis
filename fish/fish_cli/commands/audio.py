"""Audio generation commands."""

import click

from fish_cli.core.client import get_client
from fish_cli.core.exceptions import FishError
from fish_cli.core.output import (
    DEFAULT_MODEL,
    FISH_MODELS,
    print_audio_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "--voice-id",
    required=True,
    help="Voice ID to use for audio generation.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(FISH_MODELS),
    default=DEFAULT_MODEL,
    help="Model to use for generation.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    voice_id: str,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate audio from text using a cloned voice (TTS).

    PROMPT is the text to convert to speech.

    Examples:

      fish generate "Hello, world!" --voice-id d7900c21663f485ab63ebdb7e5905036

      fish generate "Welcome to Fish TTS" --voice-id abc123 --model fish-tts
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="speech",
            prompt=prompt,
            voice_id=voice_id,
            model=model,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e

"""Voice cloning command for Digital Human CLI."""

import click

from digitalhuman_cli.core.client import get_client
from digitalhuman_cli.core.exceptions import DigitalHumanError
from digitalhuman_cli.core.output import (
    DEFAULT_VOICE_LANGUAGE,
    VOICE_LANGUAGES,
    print_error,
    print_json,
    print_voice_result,
)


@click.command("clone-voice")
@click.option(
    "--audio-url",
    required=True,
    help="Public URL of a clean 10-20s voice sample (.wav/.mp3/.m4a).",
)
@click.option(
    "--lang",
    type=click.Choice(VOICE_LANGUAGES),
    default=DEFAULT_VOICE_LANGUAGE,
    show_default=True,
    help="Language of the voice sample.",
)
@click.option(
    "--name",
    default=None,
    help="Optional label for the voice.",
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
def clone_voice(
    ctx: click.Context,
    audio_url: str,
    lang: str,
    name: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Clone a voice from an audio sample.

    Returns a voice_id that can be used with 'digitalhuman generate --voice-id'.

    \b
    Examples:
      digitalhuman clone-voice --audio-url https://example.com/voice.wav
      digitalhuman clone-voice --audio-url https://example.com/voice.wav --lang en
    """
    client = get_client(ctx.obj.get("token"))

    payload: dict[str, object] = {
        "audio_url": audio_url,
        "lang": lang,
    }
    if name:
        payload["name"] = name
    if async_mode:
        payload["async"] = True

    try:
        result = client.clone_voice(**payload)
        if output_json:
            print_json(result)
        else:
            print_voice_result(result)
    except DigitalHumanError as e:
        print_error(e.message)
        raise SystemExit(1) from e

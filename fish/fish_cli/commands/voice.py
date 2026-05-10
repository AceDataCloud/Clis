"""Voice cloning commands."""

import click

from fish_cli.core.client import get_client
from fish_cli.core.exceptions import FishError
from fish_cli.core.output import print_error, print_json, print_voice_result


@click.command("clone-voice")
@click.option(
    "--voice-url",
    required=True,
    help="URL of the audio file to clone the voice from.",
)
@click.option("--title", default=None, help="Title for the cloned voice.")
@click.option("--description", default=None, help="Description for the cloned voice.")
@click.option("--image-url", default=None, help="Cover image URL for the cloned voice.")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def clone_voice(
    ctx: click.Context,
    voice_url: str,
    title: str | None,
    description: str | None,
    image_url: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Clone a voice from an audio URL.

    Examples:

      fish clone-voice --voice-url https://example.com/sample.mp3

      fish clone-voice --voice-url https://example.com/sample.mp3 --title "My Voice"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.clone_voice(
            voice_url=voice_url,
            title=title,
            description=description,
            image_url=image_url,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_voice_result(result)
    except FishError as e:
        print_error(e.message)
        raise SystemExit(1) from e

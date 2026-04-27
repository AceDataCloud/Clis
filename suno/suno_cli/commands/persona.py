"""Persona management commands."""

import click

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import print_error, print_json, print_success


@click.command()
@click.argument("audio_id")
@click.option("-n", "--name", required=True, help="Name for the persona.")
@click.option("--vox-audio-id", default=None, help="Audio ID for the vocal reference.")
@click.option(
    "--vocal-start",
    type=float,
    default=None,
    help="Start time of the vocal in the audio (seconds).",
)
@click.option(
    "--vocal-end", type=float, default=None, help="End time of the vocal in the audio (seconds)."
)
@click.option("--description", default=None, help="Description of the singer's style.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def persona(
    ctx: click.Context,
    audio_id: str,
    name: str,
    vox_audio_id: str | None,
    vocal_start: float | None,
    vocal_end: float | None,
    description: str | None,
    output_json: bool,
) -> None:
    """Create a persona (saved voice style) from an existing song.

    AUDIO_ID is the ID of the song to create the persona from.

    Examples:

      suno persona abc123 --name "My Voice Style"

      suno persona abc123 --name "My Voice Style" --vox-audio-id vox456 --vocal-start 10 --vocal-end 30
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.create_persona(
            audio_id=audio_id,
            name=name,
            vox_audio_id=vox_audio_id,
            vocal_start=vocal_start,
            vocal_end=vocal_end,
            description=description,
        )
        if output_json:
            print_json(result)
        else:
            data = result.get("data", {})
            persona_id = data.get("id", "")
            if persona_id:
                print_success(f"Persona created: {name} (ID: {persona_id})")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("persona-list")
@click.argument("user_id")
@click.option("--limit", type=int, default=None, help="Maximum number of personas to return.")
@click.option("--offset", type=int, default=None, help="Number of personas to skip.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def persona_list(
    ctx: click.Context,
    user_id: str,
    limit: int | None,
    offset: int | None,
    output_json: bool,
) -> None:
    """List personas for a user.

    USER_ID is the user ID to list personas for.

    Examples:

      suno persona-list user-123

      suno persona-list user-123 --limit 10 --offset 0
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.list_personas(user_id=user_id, limit=limit, offset=offset)
        if output_json:
            print_json(result)
        else:
            data = result.get("data", [])
            if isinstance(data, list) and data:
                for item in data:
                    pid = item.get("id", "")
                    pname = item.get("name", "")
                    print_success(f"Persona: {pname} (ID: {pid})")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("persona-delete")
@click.argument("persona_id")
@click.option("--user-id", default=None, help="User ID for ownership verification.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def persona_delete(
    ctx: click.Context,
    persona_id: str,
    user_id: str | None,
    output_json: bool,
) -> None:
    """Delete a persona by ID.

    PERSONA_ID is the ID of the persona to delete.

    Examples:

      suno persona-delete persona-456

      suno persona-delete persona-456 --user-id user-123
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.delete_persona(persona_id=persona_id, user_id=user_id)
        if output_json:
            print_json(result)
        else:
            if result.get("success"):
                print_success(f"Persona deleted: {persona_id}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("upload")
@click.argument("audio_url")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upload(
    ctx: click.Context,
    audio_url: str,
    output_json: bool,
) -> None:
    """Upload an external audio file for use in subsequent operations.

    AUDIO_URL is the URL of the audio file to upload.

    Examples:

      suno upload "https://example.com/my-song.mp3"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.upload_audio(audio_url=audio_url)
        if output_json:
            print_json(result)
        else:
            data = result.get("data", {})
            upload_id = data.get("id", "")
            if upload_id:
                print_success(f"Uploaded: {upload_id}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("voices")
@click.argument("audio_url")
@click.option("-n", "--name", default=None, help="Name for the custom voice persona.")
@click.option("--description", default=None, help="Description of the custom voice persona.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def voices(
    ctx: click.Context,
    audio_url: str,
    name: str | None,
    description: str | None,
    output_json: bool,
) -> None:
    """Create a custom voice persona from an audio URL.

    AUDIO_URL must be a publicly accessible MP3 or WAV file, at least 10 seconds
    long, containing clear vocals from a single speaker without background noise.

    Examples:

      suno voices "https://example.com/my-voice.mp3" --name "My Voice"

      suno voices "https://example.com/singer.wav" --name "Singer" --description "Smooth jazz vocalist"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.create_voice(audio_url=audio_url, name=name, description=description)
        if output_json:
            print_json(result)
        else:
            data = result.get("data", {})
            voice_id = data.get("id", "")
            if voice_id:
                label = name or voice_id
                print_success(f"Voice created: {label} (ID: {voice_id})")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

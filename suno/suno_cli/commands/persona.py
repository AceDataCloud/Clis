"""Persona management commands."""

import click
from rich.table import Table

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import console, print_error, print_json, print_success


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
            persona_id = data.get("persona_id") or data.get("id", "")
            if persona_id:
                print_success(f"Persona created: {name} (ID: {persona_id})")
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
            upload_id = data.get("audio_id") or data.get("id", "")
            if upload_id:
                print_success(f"Uploaded: {upload_id}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("personas")
@click.option("--user-id", default=None, help="Optional user ID to list personas for.")
@click.option("--limit", type=int, default=None, help="Maximum number of personas to return.")
@click.option("--offset", type=int, default=None, help="Pagination offset.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def personas(
    ctx: click.Context,
    user_id: str | None,
    limit: int | None,
    offset: int | None,
    output_json: bool,
) -> None:
    """List existing personas."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.list_personas(user_id=user_id, limit=limit, offset=offset)
        if output_json:
            print_json(result)
        else:
            items = result.get("items", [])
            if not isinstance(items, list) or not items:
                print_json(result)
                return

            table = Table(title=f"Personas ({result.get('count', len(items))})")
            table.add_column("Persona ID", style="cyan")
            table.add_column("Name", style="bold")
            table.add_column("Source")
            table.add_column("Created At")

            for item in items:
                if not isinstance(item, dict):
                    continue
                table.add_row(
                    str(item.get("persona_id", "-")),
                    str(item.get("name", "-")),
                    str(item.get("source_type", "-")),
                    str(item.get("created_at", "-")),
                )

            console.print(table)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("delete-persona")
@click.argument("persona_id")
@click.option("--user-id", default=None, help="Optional user ID if required by the API.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def delete_persona(
    ctx: click.Context,
    persona_id: str,
    user_id: str | None,
    output_json: bool,
) -> None:
    """Delete a persona by ID."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.delete_persona(persona_id=persona_id, user_id=user_id)
        if output_json:
            print_json(result)
        elif result.get("success") is True:
            print_success(f"Deleted persona: {persona_id}")
        else:
            print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("voices")
@click.argument("audio_url")
@click.option("-n", "--name", default=None, help="Optional name for the created voice.")
@click.option("--description", default=None, help="Optional description for the created voice.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def voices(
    ctx: click.Context,
    audio_url: str,
    name: str | None,
    description: str | None,
    output_json: bool,
) -> None:
    """Create a voice from an external audio URL."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.create_voice(audio_url=audio_url, name=name, description=description)
        if output_json:
            print_json(result)
        else:
            task_id = result.get("task_id", "")
            data = result.get("data", {})
            persona_id = data.get("persona_id", "") if isinstance(data, dict) else ""
            voice_name = data.get("name", name or "") if isinstance(data, dict) else (name or "")
            if task_id or persona_id:
                details = []
                if voice_name:
                    details.append(f"Name: {voice_name}")
                if persona_id:
                    details.append(f"Persona ID: {persona_id}")
                if task_id:
                    details.append(f"Task ID: {task_id}")
                print_success("Voice created" + (f" ({', '.join(details)})" if details else ""))
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

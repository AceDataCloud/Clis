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
            persona_id = data.get("id", "")
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
            upload_id = data.get("id", "")
            if upload_id:
                print_success(f"Uploaded: {upload_id}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("persona-list")
@click.option("--user-id", required=True, help="User ID whose personas should be listed.")
@click.option("--limit", type=int, default=50, show_default=True, help="Maximum personas to return.")
@click.option("--offset", type=int, default=0, show_default=True, help="Number of personas to skip.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def persona_list(
    ctx: click.Context,
    user_id: str,
    limit: int,
    offset: int,
    output_json: bool,
) -> None:
    """List saved personas for a user."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.list_personas(user_id=user_id, limit=limit, offset=offset)
        if output_json:
            print_json(result)
            return

        items = result.get("items", [])
        table = Table(title=f"Personas ({result.get('count', len(items))})")
        table.add_column("Persona ID", style="cyan")
        table.add_column("Name", style="bold")
        table.add_column("Source")
        table.add_column("Description")

        for item in items:
            table.add_row(
                item.get("persona_id", ""),
                item.get("name", ""),
                item.get("source_type", ""),
                item.get("description", "") or "",
            )

        console.print(table)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("persona-delete")
@click.argument("persona_id")
@click.option("--user-id", default=None, help="Optional user ID for ownership verification.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def persona_delete(
    ctx: click.Context,
    persona_id: str,
    user_id: str | None,
    output_json: bool,
) -> None:
    """Delete a saved persona by ID."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.delete_persona(persona_id=persona_id, user_id=user_id)
        if output_json:
            print_json(result)
        elif result.get("success"):
            print_success(f"Deleted persona: {persona_id}")
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
    """Create a custom voice persona from an audio URL."""
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.create_voice(audio_url=audio_url, name=name, description=description)
        if output_json:
            print_json(result)
            return

        data = result.get("data", {})
        persona_id = data.get("persona_id", "")
        task_id = result.get("task_id", "")
        if persona_id or task_id:
            message = f"Voice persona created: {persona_id}" if persona_id else "Voice persona request queued"
            if task_id:
                message = f"{message} (task: {task_id})"
            print_success(message)
        else:
            print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

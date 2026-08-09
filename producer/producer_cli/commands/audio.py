"""Audio generation commands."""

import click

from producer_cli.core.client import get_client
from producer_cli.core.exceptions import ProducerError
from producer_cli.core.output import (
    DEFAULT_MODEL,
    PRODUCER_MODELS,
    print_audio_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(PRODUCER_MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Music generation model to use.",
)
@click.option(
    "-l",
    "--lyric",
    default=None,
    help="Song lyrics to use (supports section tags like [Verse], [Chorus]).",
)
@click.option(
    "-t",
    "--title",
    default=None,
    help="Title for the generated song.",
)
@click.option(
    "--custom",
    is_flag=True,
    default=False,
    help="Enable custom mode for full control over lyrics and style.",
)
@click.option(
    "--instrumental",
    is_flag=True,
    default=False,
    help="Generate an instrumental track (no vocals).",
)
@click.option(
    "--seed",
    default=None,
    help="Seed for reproducible generation.",
)
@click.option(
    "--sound-strength",
    default=None,
    type=float,
    help="Strength of the sound style (0.0-1.0).",
)
@click.option(
    "--lyrics-strength",
    default=None,
    type=float,
    help="Strength of the lyrics adherence (0.0-1.0).",
)
@click.option(
    "--weirdness",
    default=None,
    type=float,
    help="Weirdness factor for generation (0.0-1.0).",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    lyric: str | None,
    title: str | None,
    custom: bool,
    instrumental: bool,
    seed: str | None,
    sound_strength: float | None,
    lyrics_strength: float | None,
    weirdness: float | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a music track from a text prompt.

    PROMPT is a description of the music style or theme to generate.

    \b
    Examples:
      producer generate "A happy upbeat pop song about summer"
      producer generate "Dark metal with heavy guitar riffs" -m "FUZZ-2.0 Pro"
      producer generate "Jazz instrumental" --instrumental
      producer generate "Epic orchestral battle theme" --custom -l "[Verse]\\nHere we stand"
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "generate",
        "prompt": prompt,
        "model": model,
        "lyric": lyric or "",
        "title": title,
        "custom": custom if custom else None,
        "instrumental": instrumental if instrumental else None,
        "seed": seed,
        "sound_strength": sound_strength,
        "lyrics_strength": lyrics_strength,
        "weirdness": weirdness,
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option(
    "-m",
    "--model",
    type=click.Choice(PRODUCER_MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Music generation model to use.",
)
@click.option(
    "--prompt",
    default=None,
    help="Style description for the cover.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def cover(
    ctx: click.Context,
    audio_id: str,
    model: str,
    prompt: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Create a cover version of an existing audio track.

    AUDIO_ID is the ID of the audio track to create a cover of.

    \b
    Examples:
      producer cover abc123-def456
      producer cover abc123 --prompt "Make it more upbeat"
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "cover",
        "audio_id": audio_id,
        "model": model,
        "prompt": prompt or "",
        "lyric": "",
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option(
    "-m",
    "--model",
    type=click.Choice(PRODUCER_MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Music generation model to use.",
)
@click.option(
    "--prompt",
    default=None,
    help="Style description for the extension.",
)
@click.option(
    "--continue-at",
    default=None,
    type=float,
    help="Timestamp (in seconds) to continue from.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def extend(
    ctx: click.Context,
    audio_id: str,
    model: str,
    prompt: str | None,
    continue_at: float | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Extend an existing audio track.

    AUDIO_ID is the ID of the audio track to extend.

    \b
    Examples:
      producer extend abc123-def456
      producer extend abc123 --continue-at 30.5
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "extend",
        "audio_id": audio_id,
        "model": model,
        "prompt": prompt or "",
        "lyric": "",
        "continue_at": continue_at,
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option(
    "-m",
    "--model",
    type=click.Choice(PRODUCER_MODELS),
    default=DEFAULT_MODEL,
    show_default=True,
    help="Music generation model to use.",
)
@click.option(
    "--prompt",
    default=None,
    help="Style description for the variation.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def variation(
    ctx: click.Context,
    audio_id: str,
    model: str,
    prompt: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a variation of an existing audio track.

    AUDIO_ID is the ID of the audio track to create a variation of.

    \b
    Examples:
      producer variation abc123-def456
      producer variation abc123 --prompt "More energetic version"
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "variation",
        "audio_id": audio_id,
        "model": model,
        "prompt": prompt or "",
        "lyric": "",
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("swap-vocals")
@click.argument("audio_id")
@click.option(
    "--prompt",
    default=None,
    help="Style description for the vocal swap.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def swap_vocals(
    ctx: click.Context,
    audio_id: str,
    prompt: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Swap the vocals in an existing audio track.

    AUDIO_ID is the ID of the audio track whose vocals to swap.

    \b
    Examples:
      producer swap-vocals abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "swap_vocals",
        "audio_id": audio_id,
        "prompt": prompt or "",
        "lyric": "",
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("swap-instrumentals")
@click.argument("audio_id")
@click.option(
    "--prompt",
    default=None,
    help="Style description for the instrumental swap.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def swap_instrumentals(
    ctx: click.Context,
    audio_id: str,
    prompt: str | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Swap the instrumentals in an existing audio track.

    AUDIO_ID is the ID of the audio track whose instrumentals to swap.

    \b
    Examples:
      producer swap-instrumentals abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "swap_instrumentals",
        "audio_id": audio_id,
        "prompt": prompt or "",
        "lyric": "",
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("replace-section")
@click.argument("audio_id")
@click.option(
    "--prompt",
    default=None,
    help="Style/content description for the replacement section.",
)
@click.option(
    "--replace-section-start",
    default=None,
    type=float,
    help="Start time (in seconds) of the section to replace.",
)
@click.option(
    "--replace-section-end",
    default=None,
    type=float,
    help="End time (in seconds) of the section to replace.",
)
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def replace_section(
    ctx: click.Context,
    audio_id: str,
    prompt: str | None,
    replace_section_start: float | None,
    replace_section_end: float | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Replace a section of an existing audio track.

    AUDIO_ID is the ID of the audio track to modify.

    \b
    Examples:
      producer replace-section abc123 --replace-section-start 10 --replace-section-end 30
      producer replace-section abc123 --prompt "Add a guitar solo" --replace-section-start 45
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "replace_section",
        "audio_id": audio_id,
        "prompt": prompt or "",
        "lyric": "",
        "replace_section_start": replace_section_start,
        "replace_section_end": replace_section_end,
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option(
    "--callback-url",
    default=None,
    help="Optional callback URL for async generation.",
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
def stems(
    ctx: click.Context,
    audio_id: str,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Extract stems (vocals, instruments) from an existing audio track.

    AUDIO_ID is the ID of the audio track to extract stems from.

    \b
    Examples:
      producer stems abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "stems",
        "audio_id": audio_id,
        "prompt": "",
        "lyric": "",
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except ProducerError as e:
        print_error(e.message)
        raise SystemExit(1) from e

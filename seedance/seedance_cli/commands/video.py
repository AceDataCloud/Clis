"""Video generation commands."""

import json

import click

from seedance_cli.core.client import get_client
from seedance_cli.core.exceptions import SeedanceError
from seedance_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_ASPECT_RATIO,
    DEFAULT_MODEL,
    RESOLUTIONS,
    SEEDANCE_MODELS,
    print_error,
    print_json,
    print_video_result,
)


def _shared_video_options(f):  # type: ignore[no-untyped-def]
    """Decorator that attaches options shared by generate and image-to-video."""
    decorators = [
        click.option(
            "-m",
            "--model",
            type=click.Choice(SEEDANCE_MODELS),
            default=DEFAULT_MODEL,
            help="Seedance model version.",
        ),
        click.option(
            "-a",
            "--aspect-ratio",
            type=click.Choice(ASPECT_RATIOS),
            default=DEFAULT_ASPECT_RATIO,
            help="Aspect ratio of the output.",
        ),
        click.option(
            "-r",
            "--resolution",
            type=click.Choice(RESOLUTIONS),
            default=None,
            help="Output resolution.",
        ),
        click.option(
            "--duration",
            type=click.IntRange(-1, 30),
            default=None,
            help="Duration in seconds (-1 for auto, up to 15 for 2.0 or 30 for 2.5). Mutually exclusive with --frames.",
        ),
        click.option(
            "--frames",
            type=click.IntRange(29, 289),
            default=None,
            help="Frame count (29-289, must satisfy 25+4n). Mutually exclusive with --duration.",
        ),
        click.option(
            "--seed",
            type=click.IntRange(-1, 4294967295),
            default=None,
            help="Random seed for reproducible generation (-1 for random).",
        ),
        click.option(
            "--camerafixed",
            type=click.BOOL,
            default=None,
            help="Fix the camera position during generation (true/false).",
        ),
        click.option(
            "--watermark",
            type=click.BOOL,
            default=None,
            help="Add a watermark to the generated video (true/false).",
        ),
        click.option(
            "--generate-audio",
            type=click.BOOL,
            default=None,
            help="Generate audio for the video (true/false). Supported by Seedance 1.5 Pro and 2.x.",
        ),
        click.option(
            "--return-last-frame",
            type=click.BOOL,
            default=None,
            help="Return the last frame of the generated video (true/false).",
        ),
        click.option(
            "--task-type",
            type=click.Choice(["auto", "edit", "extend"]),
            default=None,
            help="Seedance 2.5 task type.",
        ),
        click.option(
            "--output-format",
            type=click.Choice(["mp4", "mov"]),
            default=None,
            help="Seedance 2.5 output format.",
        ),
        click.option(
            "--tool-json",
            "tool_jsons",
            multiple=True,
            help="Seedance 2.5 web_search tool object as JSON.",
        ),
        click.option(
            "--priority",
            type=click.IntRange(0, 9),
            default=None,
            help="Seedance 2.5 task priority (0-9).",
        ),
        click.option(
            "--safety-identifier",
            default=None,
            help="Stable anonymous end-user identifier (maximum 64 characters).",
        ),
        click.option(
            "--execution-expires-after",
            type=click.IntRange(3600, 259200),
            default=None,
            help="Task timeout threshold in seconds (3600-259200).",
        ),
        click.option("--callback-url", default=None, help="Webhook callback URL."),
        click.option(
            "--first-frame-url",
            default=None,
            help="Reference image URL to use as the first frame.",
        ),
        click.option(
            "--last-frame-url",
            default=None,
            help="Reference image URL to use as the last frame.",
        ),
        click.option(
            "--reference-image-url",
            "reference_image_urls",
            multiple=True,
            help="Additional reference image URL(s). Can be specified multiple times.",
        ),
        click.option(
            "--audio-url",
            default=None,
            help="Reference audio URL.",
        ),
        click.option(
            "--video-url",
            default=None,
            help="Reference video URL.",
        ),
        click.option(
            "--async",
            "async_mode",
            is_flag=True,
            default=False,
            help="Submit asynchronously; returns a task_id to poll instead of waiting.",
        ),
        click.option("--json", "output_json", is_flag=True, help="Output raw JSON."),
    ]
    for decorator in reversed(decorators):
        f = decorator(f)
    return f


def _build_common_payload(
    model: str,
    aspect_ratio: str,
    resolution: str | None,
    duration: int | None,
    frames: int | None,
    seed: int | None,
    camerafixed: bool | None,
    watermark: bool | None,
    generate_audio: bool | None,
    return_last_frame: bool | None,
    task_type: str | None,
    output_format: str | None,
    tool_jsons: tuple[str, ...],
    priority: int | None,
    safety_identifier: str | None,
    execution_expires_after: int | None,
    callback_url: str | None,
    async_mode: bool,
) -> dict[str, object]:
    """Build the common parts of a video generation payload."""
    payload: dict[str, object] = {
        "model": model,
        "ratio": aspect_ratio,
    }
    if resolution is not None:
        payload["resolution"] = resolution
    if duration is not None:
        payload["duration"] = duration
    if frames is not None:
        payload["frames"] = frames
    if seed is not None:
        payload["seed"] = seed
    if camerafixed is not None:
        payload["camerafixed"] = camerafixed
    if watermark is not None:
        payload["watermark"] = watermark
    if generate_audio is not None:
        payload["generate_audio"] = generate_audio
    if return_last_frame is not None:
        payload["return_last_frame"] = return_last_frame
    if task_type is not None:
        payload["omni_reference_task_type"] = task_type
    if output_format is not None:
        payload["output_format"] = output_format
    if tool_jsons:
        payload["tools"] = _parse_tools(tool_jsons)
    if priority is not None:
        payload["priority"] = priority
    if safety_identifier is not None:
        if len(safety_identifier) > 64:
            raise click.UsageError("--safety-identifier must be at most 64 characters.")
        payload["safety_identifier"] = safety_identifier
    if execution_expires_after is not None:
        payload["execution_expires_after"] = execution_expires_after
    if callback_url is not None:
        payload["callback_url"] = callback_url
    if async_mode:
        payload["async"] = True
    return payload


def _parse_tools(tool_jsons: tuple[str, ...]) -> list[dict[str, object]]:
    """Parse and validate the Seedance web search tool."""
    if len(tool_jsons) > 1:
        raise click.UsageError("--tool-json may only be specified once.")
    try:
        tool = json.loads(tool_jsons[0])
    except json.JSONDecodeError as exc:
        raise click.UsageError(f"Invalid --tool-json: {exc.msg}") from exc
    if not isinstance(tool, dict):
        raise click.UsageError("--tool-json must decode to a JSON object.")

    allowed_keys = {"type", "limit", "max_keyword", "sources"}
    if unknown_keys := tool.keys() - allowed_keys:
        raise click.UsageError(f"Invalid --tool-json field(s): {', '.join(sorted(unknown_keys))}.")
    if tool.get("type") != "web_search":
        raise click.UsageError('--tool-json requires "type": "web_search".')
    for field in ("limit", "max_keyword"):
        value = tool.get(field)
        if field in tool and (
            not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 50
        ):
            raise click.UsageError(f'--tool-json "{field}" must be an integer from 1 to 50.')
    sources = tool.get("sources")
    allowed_sources = {"toutiao", "douyin", "moji", "search_engine"}
    if "sources" in tool and (
        not isinstance(sources, list)
        or any(not isinstance(source, str) or source not in allowed_sources for source in sources)
    ):
        raise click.UsageError(
            '--tool-json "sources" must contain only toutiao, douyin, moji, or search_engine.'
        )
    return [tool]


def _build_content(
    prompt: str,
    first_frame_url: str | None,
    last_frame_url: str | None,
    reference_image_urls: tuple[str, ...],
    audio_url: str | None,
    video_url: str | None,
) -> list[dict[str, object]]:
    """Build request content items from the supported reference media inputs."""
    content: list[dict[str, object]] = [{"type": "text", "text": prompt}]
    image_sources = [
        (first_frame_url, "first_frame"),
        (last_frame_url, "last_frame"),
    ]
    image_sources.extend((url, "reference_image") for url in reference_image_urls)
    for url, role in image_sources:
        if url is not None:
            content.append({"type": "image_url", "role": role, "image_url": {"url": url}})
    if audio_url is not None:
        content.append(
            {
                "type": "audio_url",
                "role": "reference_audio",
                "audio_url": {"url": audio_url},
            }
        )
    if video_url is not None:
        content.append(
            {
                "type": "video_url",
                "role": "reference_video",
                "video_url": {"url": video_url},
            }
        )
    return content


@click.command()
@click.argument("prompt")
@_shared_video_options
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    aspect_ratio: str,
    resolution: str | None,
    duration: int | None,
    frames: int | None,
    seed: int | None,
    camerafixed: bool | None,
    watermark: bool | None,
    generate_audio: bool | None,
    return_last_frame: bool | None,
    task_type: str | None,
    output_format: str | None,
    tool_jsons: tuple[str, ...],
    priority: int | None,
    safety_identifier: str | None,
    execution_expires_after: int | None,
    callback_url: str | None,
    first_frame_url: str | None,
    last_frame_url: str | None,
    reference_image_urls: tuple[str, ...],
    audio_url: str | None,
    video_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      seedance generate "A cinematic scene of a sunset over the ocean"

      seedance generate "A cat playing with yarn" -m doubao-seedance-1-5-pro-251215
    """
    if duration is not None and frames is not None:
        raise click.UsageError("--duration and --frames are mutually exclusive.")
    if len(prompt) > 1000:
        raise click.UsageError("PROMPT must be at most 1000 characters.")

    client = get_client(ctx.obj.get("token"))
    try:
        payload = _build_common_payload(
            model=model,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration=duration,
            frames=frames,
            seed=seed,
            camerafixed=camerafixed,
            watermark=watermark,
            generate_audio=generate_audio,
            return_last_frame=return_last_frame,
            task_type=task_type,
            output_format=output_format,
            tool_jsons=tool_jsons,
            priority=priority,
            safety_identifier=safety_identifier,
            execution_expires_after=execution_expires_after,
            callback_url=callback_url,
            async_mode=async_mode,
        )
        payload["content"] = _build_content(
            prompt=prompt,
            first_frame_url=first_frame_url,
            last_frame_url=last_frame_url,
            reference_image_urls=reference_image_urls,
            audio_url=audio_url,
            video_url=video_url,
        )

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except SeedanceError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    "image_urls",
    required=True,
    multiple=True,
    help="Image URL(s) for reference. Can be specified multiple times.",
)
@_shared_video_options
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    aspect_ratio: str,
    resolution: str | None,
    duration: int | None,
    frames: int | None,
    seed: int | None,
    camerafixed: bool | None,
    watermark: bool | None,
    generate_audio: bool | None,
    return_last_frame: bool | None,
    task_type: str | None,
    output_format: str | None,
    tool_jsons: tuple[str, ...],
    priority: int | None,
    safety_identifier: str | None,
    execution_expires_after: int | None,
    callback_url: str | None,
    first_frame_url: str | None,
    last_frame_url: str | None,
    reference_image_urls: tuple[str, ...],
    audio_url: str | None,
    video_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s).

    PROMPT describes the desired video. Provide one or more image URLs as reference.

    Examples:

      seedance image-to-video "Animate this scene" -i https://example.com/photo.jpg

      seedance image-to-video "Bring to life" -i img1.jpg -i img2.jpg
    """
    if duration is not None and frames is not None:
        raise click.UsageError("--duration and --frames are mutually exclusive.")
    if len(prompt) > 1000:
        raise click.UsageError("PROMPT must be at most 1000 characters.")

    client = get_client(ctx.obj.get("token"))
    try:
        payload = _build_common_payload(
            model=model,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration=duration,
            frames=frames,
            seed=seed,
            camerafixed=camerafixed,
            watermark=watermark,
            generate_audio=generate_audio,
            return_last_frame=return_last_frame,
            task_type=task_type,
            output_format=output_format,
            tool_jsons=tool_jsons,
            priority=priority,
            safety_identifier=safety_identifier,
            execution_expires_after=execution_expires_after,
            callback_url=callback_url,
            async_mode=async_mode,
        )
        payload["content"] = _build_content(
            prompt=prompt,
            first_frame_url=first_frame_url,
            last_frame_url=last_frame_url,
            reference_image_urls=image_urls + reference_image_urls,
            audio_url=audio_url,
            video_url=video_url,
        )

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except SeedanceError as e:
        print_error(e.message)
        raise SystemExit(1) from e

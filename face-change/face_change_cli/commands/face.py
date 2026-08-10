"""Face transformation commands."""

import json
from typing import Any

import click

from face_change_cli.core.client import get_client
from face_change_cli.core.exceptions import FaceChangeError
from face_change_cli.core.output import print_error, print_json, print_result


def _parse_json_array(value: str, option_name: str) -> list[Any]:
    """Parse a JSON array option."""
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be a valid JSON array.") from exc
    if not isinstance(parsed, list):
        raise click.BadParameter(f"{option_name} must be a valid JSON array.")
    return parsed


def _emit(client_method: Any, payload: dict[str, object], output_json: bool, title: str) -> None:
    """Call a client method and print the result."""
    try:
        result = client_method(**payload)
        if output_json:
            print_json(result)
        else:
            print_result(result, title=title)
    except FaceChangeError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("image_url")
@click.option("--mode", type=float, default=None, help="Face analysis mode.")
@click.option("--face-model-version", default=None, help="Face model version to use.")
@click.option("--need-rotate-detection", type=float, default=None, help="Enable rotate detection flag.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def analyze(
    ctx: click.Context,
    image_url: str,
    mode: float | None,
    face_model_version: str | None,
    need_rotate_detection: float | None,
    output_json: bool,
) -> None:
    """Analyze facial landmarks in an image."""
    payload: dict[str, object] = {
        "image_url": image_url,
        "mode": mode,
        "face_model_version": face_model_version,
        "need_rotate_detection": need_rotate_detection,
    }
    _emit(get_client(ctx.obj.get("token")).analyze, payload, output_json, "Analyze Result")


@click.command()
@click.argument("image_url")
@click.option("--smoothing", type=float, default=None, help="Skin smoothing level.")
@click.option("--whitening", type=float, default=None, help="Skin whitening level.")
@click.option("--face-lifting", type=float, default=None, help="Face lifting level.")
@click.option("--eye-enlarging", type=float, default=None, help="Eye enlarging level.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def beautify(
    ctx: click.Context,
    image_url: str,
    smoothing: float | None,
    whitening: float | None,
    face_lifting: float | None,
    eye_enlarging: float | None,
    output_json: bool,
) -> None:
    """Beautify a face image."""
    payload: dict[str, object] = {
        "image_url": image_url,
        "smoothing": smoothing,
        "whitening": whitening,
        "face_lifting": face_lifting,
        "eye_enlarging": eye_enlarging,
    }
    _emit(get_client(ctx.obj.get("token")).beautify, payload, output_json, "Beautify Result")


@click.command("change-age")
@click.argument("image_url")
@click.option("--age-infos", required=True, help="Age info array as JSON.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def change_age(ctx: click.Context, image_url: str, age_infos: str, output_json: bool) -> None:
    """Change the age of faces in an image."""
    payload: dict[str, object] = {
        "image_url": image_url,
        "age_infos": _parse_json_array(age_infos, "--age-infos"),
    }
    _emit(get_client(ctx.obj.get("token")).change_age, payload, output_json, "Change Age Result")


@click.command("change-gender")
@click.argument("image_url")
@click.option("--gender-infos", required=True, help="Gender info array as JSON.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def change_gender(ctx: click.Context, image_url: str, gender_infos: str, output_json: bool) -> None:
    """Change the gender of faces in an image."""
    payload: dict[str, object] = {
        "image_url": image_url,
        "gender_infos": _parse_json_array(gender_infos, "--gender-infos"),
    }
    _emit(
        get_client(ctx.obj.get("token")).change_gender,
        payload,
        output_json,
        "Change Gender Result",
    )


@click.command("detect-live")
@click.argument("image_url")
@click.option("--face-model-version", type=float, default=None, help="Face model version to use.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def detect_live(
    ctx: click.Context,
    image_url: str,
    face_model_version: float | None,
    output_json: bool,
) -> None:
    """Detect whether a face image is live."""
    payload: dict[str, object] = {
        "image_url": image_url,
        "face_model_version": face_model_version,
    }
    _emit(get_client(ctx.obj.get("token")).detect_live, payload, output_json, "Detect Live Result")


@click.command()
@click.option("--source-image-url", default=None, help="Source face image URL.")
@click.option("--target-image-url", default=None, help="Target image URL.")
@click.option("--timeout", type=float, default=None, help="Request timeout in seconds.")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--async",
    "async_mode",
    is_flag=True,
    default=False,
    help="Submit asynchronously; returns a task_id to poll instead of waiting.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def swap(
    ctx: click.Context,
    source_image_url: str | None,
    target_image_url: str | None,
    timeout: float | None,
    callback_url: str | None,
    async_mode: bool,
    output_json: bool,
) -> None:
    """Swap a source face into a target image."""
    payload: dict[str, object] = {
        "source_image_url": source_image_url,
        "target_image_url": target_image_url,
        "timeout": timeout,
        "callback_url": callback_url,
        "async": async_mode if async_mode else None,
    }
    _emit(get_client(ctx.obj.get("token")).swap, payload, output_json, "Swap Result")


@click.command()
@click.argument("image_url")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def cartoon(ctx: click.Context, image_url: str, output_json: bool) -> None:
    """Generate a cartoon image from a face photo."""
    _emit(
        get_client(ctx.obj.get("token")).cartoon,
        {"image_url": image_url},
        output_json,
        "Cartoon Result",
    )

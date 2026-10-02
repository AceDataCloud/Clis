"""Structured FLUX video commands."""

import json
from pathlib import Path
from typing import Any

import click
from pydantic import TypeAdapter, ValidationError

from flux_cli.core.client import get_client
from flux_cli.core.exceptions import FluxError
from flux_cli.core.output import print_error, print_json
from flux_cli.core.video_types import FluxVideoRequest


def _request(ctx: click.Context, request_file: Path) -> None:
    try:
        body = json.loads(request_file.read_text(encoding="utf-8"))
        request: Any = TypeAdapter(FluxVideoRequest).validate_python(body)
    except (OSError, ValueError, ValidationError) as error:
        raise click.BadParameter(str(error), param_hint="--request-file") from error
    try:
        result = get_client(ctx.obj.get("token")).request(
            "/flux/videos", request.model_dump(mode="json", by_alias=True, exclude_none=True)
        )
        print_json(result)
    except FluxError as error:
        print_error(error.message)
        raise SystemExit(1) from error


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def video(ctx: click.Context, request_file: Path) -> None:
    """Generate FLUX videos from JSON. Poll with task/wait."""
    _request(ctx, request_file)

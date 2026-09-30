"""Kling platform asset management and references."""

import json
from pathlib import Path
from typing import Any

import click
from pydantic import TypeAdapter, ValidationError

from kling_cli.core.asset_types import (
    AssetManagementRequest,
    AssetVideoRequest,
    VoiceCreationRequest,
)
from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.output import print_error, print_json


def _request(ctx: click.Context, request_file: Path, schema: Any, endpoint: str) -> None:
    try:
        body = json.loads(request_file.read_text(encoding="utf-8"))
        request = TypeAdapter(schema).validate_python(body)
    except (OSError, ValueError, ValidationError) as error:
        raise click.BadParameter(str(error), param_hint="--request-file") from error
    try:
        result = get_client(ctx.obj.get("token")).request(
            endpoint, request.model_dump(mode="json", by_alias=True, exclude_none=True)
        )
        print_json(result)
    except KlingError as error:
        print_error(error.message)
        raise SystemExit(1) from error


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def elements(ctx: click.Context, request_file: Path) -> None:
    """Manage owned/preset element platform IDs. Custom creation is unavailable."""
    _request(ctx, request_file, AssetManagementRequest, "/kling/elements")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def voices(ctx: click.Context, request_file: Path) -> None:
    """Create voices (0.07 Credits) or manage owned/preset voice platform IDs."""
    _request(ctx, request_file, AssetManagementRequest | VoiceCreationRequest, "/kling/voices")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def asset_video(ctx: click.Context, request_file: Path) -> None:
    """Generate using platform element or voice references; specified voices cost 1.68 Credits/s."""
    _request(ctx, request_file, AssetVideoRequest, "/kling/videos")

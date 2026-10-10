"""Structured MiniMax native commands."""

import json
from pathlib import Path
from typing import Any

import click
from pydantic import TypeAdapter, ValidationError

from minimax_cli.core.client import get_client
from minimax_cli.core.exceptions import MiniMaxError
from minimax_cli.core.native_types import (
    MaxVideoRequest,
    PromptEnhancementRequest,
    RegenerationRequest,
)
from minimax_cli.core.output import print_error, print_json


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
    except MiniMaxError as error:
        print_error(error.message)
        raise SystemExit(1) from error


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def max_video(ctx: click.Context, request_file: Path) -> None:
    """Generate H3 Max 480P/768P video, 5–15 seconds, from JSON. Poll with task/wait."""
    _request(ctx, request_file, MaxVideoRequest, "/minimax/videos")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def enhance_prompt(ctx: click.Context, request_file: Path) -> None:
    """Enhance an H3 prompt and materials from JSON. Poll with task/wait."""
    _request(ctx, request_file, PromptEnhancementRequest, "/minimax/prompt-enhancement")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def regenerate(ctx: click.Context, request_file: Path) -> None:
    """Regenerate owned H3 768P at 2K, or provide the exact original materials plus base_video. Poll with task/wait."""
    _request(ctx, request_file, RegenerationRequest, "/minimax/regenerate")

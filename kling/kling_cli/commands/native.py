"""Typed Kling native video and commerce commands."""

import json
from pathlib import Path
from typing import Any

import click
from pydantic import TypeAdapter, ValidationError

from kling_cli.core.client import get_client
from kling_cli.core.exceptions import KlingError
from kling_cli.core.native_types import (
    ApparelRequest,
    CommerceRequest,
    GoodsRequest,
    StoryboardRequest,
    TryOnRequest,
    TurboRequest,
)
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
def turbo(ctx: click.Context, request_file: Path) -> None:
    """Generate V3 Turbo with native audio; no off switch. Poll with task/wait."""
    _request(ctx, request_file, TurboRequest, "/kling/videos")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def storyboard(ctx: click.Context, request_file: Path) -> None:
    """Generate automatic or customized V3/V3 Omni multishot video. Poll with task/wait."""
    _request(ctx, request_file, StoryboardRequest, "/kling/videos")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def apparel(ctx: click.Context, request_file: Path) -> None:
    """Generate apparel demonstration video. Poll with task/wait."""
    _request(ctx, request_file, ApparelRequest, "/kling/apparel")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def goods_studio(ctx: click.Context, request_file: Path) -> None:
    """Generate product studio video. Poll with task/wait."""
    _request(ctx, request_file, GoodsRequest, "/kling/goods-studio")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def video_commerce(ctx: click.Context, request_file: Path) -> None:
    """Generate creator or product voiceover. Poll with task/wait."""
    _request(ctx, request_file, CommerceRequest, "/kling/video-commerce")


@click.command()
@click.option(
    "--request-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True
)
@click.pass_context
def virtual_try_on(ctx: click.Context, request_file: Path) -> None:
    """Generate try-on images. Poll with task/wait."""
    _request(ctx, request_file, TryOnRequest, "/kling/virtual-try-on")

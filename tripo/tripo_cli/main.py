"""Submit Tripo operations and retrieve the original task."""

import json
from typing import Any

import click
import httpx


@click.group()
@click.option(
    "--token", envvar="ACEDATACLOUD_API_TOKEN", help="Ace application API token."
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Generate 3D assets, process models and retrieve results."""
    ctx.obj = token


def post(resource: str, body: dict[str, Any], key: str | None = None) -> None:
    token = click.get_current_context().obj
    if not token:
        raise click.ClickException("Set ACEDATACLOUD_API_TOKEN or supply --token.")
    headers = {"Authorization": f"Bearer {token}"}
    if key:
        headers["Idempotency-Key"] = key
    try:
        response = httpx.post(
            f"https://api.acedata.cloud/tripo/{resource}",
            json=body,
            headers=headers,
            timeout=90,
        )
        response.raise_for_status()
        result = response.json()
    except httpx.HTTPStatusError as exc:
        raise click.ClickException(
            f"HTTP {exc.response.status_code}: {exc.response.text}"
        ) from exc
    except (httpx.RequestError, ValueError) as exc:
        raise click.ClickException(
            "Response unavailable. Reuse the original task ID or idempotency key before retrying."
        ) from exc
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


def request_body(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except ValueError as exc:
        raise click.BadParameter(
            "Expected a JSON object.", param_hint="--json"
        ) from exc
    if not isinstance(value, dict):
        raise click.BadParameter("Expected a JSON object.", param_hint="--json")
    return value


@cli.command()
@click.option(
    "--json",
    "payload",
    required=True,
    help="Generation inputs such as prompt, image_url or image_urls.",
)
@click.option(
    "--idempotency-key", help="Reuse this value and the same inputs on retry."
)
def generate(payload: str, idempotency_key: str | None) -> None:
    """Generate a model from text, an image or multiple views."""
    body = request_body(payload)
    body.setdefault("async", True)
    post("generations", body, idempotency_key)


def process(resource: str, action: str, payload: str, key: str | None) -> None:
    body = request_body(payload)
    if body.get("action", action) != action:
        raise click.BadParameter("The JSON action must match the selected command.")
    body["action"] = action
    body.setdefault("async", True)
    post(resource, body, key)


@cli.command()
@click.argument("action", type=click.Choice(["import", "texture", "convert"]))
@click.option(
    "--json",
    "payload",
    required=True,
    help="Model input and operation-specific options.",
)
@click.option("--idempotency-key")
def models(action: str, payload: str, idempotency_key: str | None) -> None:
    """Import, texture or convert a model."""
    process("models", action, payload, idempotency_key)


@cli.command()
@click.argument("action", type=click.Choice(["rig_check", "rig", "retarget"]))
@click.option(
    "--json", "payload", required=True, help="Model input and animation options."
)
@click.option("--idempotency-key")
def animations(action: str, payload: str, idempotency_key: str | None) -> None:
    """Check riggability, bind a skeleton or retarget animation."""
    process("animations", action, payload, idempotency_key)


@cli.command()
@click.argument("ids", nargs=-1, required=True)
@click.option("--trace", is_flag=True, help="Interpret IDs as trace IDs.")
@click.option(
    "--batch", is_flag=True, help="Return the batch envelope even for one ID."
)
def tasks(ids: tuple[str, ...], trace: bool, batch: bool) -> None:
    """Retrieve tasks. Multiple IDs are returned in input order."""
    if len(ids) > 100:
        raise click.UsageError("Provide up to 100 IDs per request.")
    field = "trace_id" if trace else "id"
    if batch or len(ids) > 1:
        post("tasks", {"action": "retrieve_batch", field + "s": list(ids)})
    else:
        post("tasks", {field: ids[0]})

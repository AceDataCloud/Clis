"""Helpers for parsing JSON-valued CLI options."""

import json
from typing import Any

import click


def parse_json_value(value: str | None, option_name: str) -> Any:
    """Parse a CLI option as JSON."""
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{option_name} must be valid JSON.") from exc


def parse_json_object(value: str | None, option_name: str) -> dict[str, Any] | None:
    """Parse a CLI option as a JSON object."""
    parsed = parse_json_value(value, option_name)
    if parsed is None:
        return None
    if not isinstance(parsed, dict):
        raise click.BadParameter(f"{option_name} must be a JSON object.")
    return parsed


def parse_json_array(value: str | None, option_name: str) -> list[Any] | None:
    """Parse a CLI option as a JSON array."""
    parsed = parse_json_value(value, option_name)
    if parsed is None:
        return None
    if not isinstance(parsed, list):
        raise click.BadParameter(f"{option_name} must be a JSON array.")
    return parsed


def parse_json_or_string(value: str | None, option_name: str) -> Any:
    """Parse JSON when possible, otherwise keep plain strings."""
    if value is None:
        return None
    stripped = value.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        return parse_json_value(value, option_name)
    return value

"""Localization translation command."""

import json
from typing import Any

import click

from localization_cli.core.client import get_client
from localization_cli.core.exceptions import LocalizationError
from localization_cli.core.output import print_error, print_json, print_translation_result

LOCALES = (
    "en",
    "de",
    "pt",
    "es",
    "fr",
    "zh-CN",
    "zh-TW",
    "it",
    "ko",
    "ja",
    "ru",
    "pl",
    "fi",
    "sv",
    "el",
    "uk",
    "ar",
    "sr",
)


def parse_input(value: str, extension: str) -> str | dict[str, Any]:
    """Parse CLI input according to the selected localization file extension."""
    if extension != "json":
        return value

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as e:
        raise click.BadParameter("must be a valid JSON object when --extension json") from e

    if not isinstance(parsed, dict):
        raise click.BadParameter("must be a JSON object when --extension json")

    return parsed


@click.command()
@click.argument("input_text", metavar="INPUT")
@click.option("--locale", required=True, type=click.Choice(LOCALES), help="Localization Translate Locale.")
@click.option(
    "--extension",
    default="md",
    show_default=True,
    type=click.Choice(("md", "json")),
    help="Localization Translate Extension.",
)
@click.option(
    "--model",
    type=click.Choice(("gpt-3.5", "gpt-4")),
    help="Localization Translate Model.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def translate(
    ctx: click.Context,
    input_text: str,
    locale: str,
    extension: str,
    model: str | None,
    output_json: bool,
) -> None:
    """Translate a JSON input into any localized file.

    INPUT is markdown text for --extension md, or a JSON object string for --extension json.

    \b
    Examples:
      localization translate "# Title" --locale zh-CN
      localization translate '{"message.clickButton":{"message":"Please click"}}' --extension json --locale zh-CN
    """
    client = get_client(ctx.obj.get("token"))

    try:
        payload: dict[str, Any] = {
            "input": parse_input(input_text, extension),
            "locale": locale,
            "extension": extension,
            "model": model,
        }
        result = client.translate(**payload)
        if output_json:
            print_json(result)
        else:
            print_translation_result(result)
    except click.BadParameter as e:
        raise click.ClickException(str(e)) from e
    except LocalizationError as e:
        print_error(e.message)
        raise SystemExit(1) from e

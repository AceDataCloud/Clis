"""Find independently installable service packages without credentials/network."""

import json
import re
from importlib.resources import files

import click


def _search_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


@click.command("packages")
@click.argument("query", required=False, default="")
@click.option(
    "--json", "output_json", is_flag=True, help="Output package identities and install state."
)
def packages(query: str, output_json: bool) -> None:
    """Find Suno, Seedance, HappyHorse, GPT Image or Nano Banana packages.

    This is an offline package directory, not a generation or install command.
    """
    data = json.loads(files("adc_cli").joinpath("service_packages.json").read_text())
    needle = _search_key(query)
    matches = [
        entry
        for entry in data["services"]
        if any(
            needle in _search_key(value)
            for value in [
                entry["slug"],
                entry["label"],
                *entry["search_terms"],
                entry["cli_package"],
                entry["mcp_package"],
            ]
        )
    ]
    if output_json:
        click.echo(json.dumps({**data, "services": matches}, ensure_ascii=False, indent=2))
        return
    click.echo(f"Service packages by Ace Data Cloud (catalog checked {data['evidence_date']})")
    for entry in matches:
        click.echo(f"\n{entry['brand']}")
        if entry["cli_published"]:
            click.echo(f"  CLI: python -m pip install {entry['cli_package']}")
            click.echo(f"       https://pypi.org/project/{entry['cli_package']}/")
        else:
            click.echo(
                f"  CLI: source only; {entry['cli_package']} is not a verified published package"
            )
        click.echo(f"  MCP: https://pypi.org/project/{entry['mcp_package']}/")
        click.echo(f"  Local check: {entry['safe_command']}")
        click.echo(f"  {entry['note']}")
    if not matches:
        click.echo("No matching service in this package directory.")
    click.echo(
        "\nCheck package publisher, current version, service access and pricing before API use."
    )

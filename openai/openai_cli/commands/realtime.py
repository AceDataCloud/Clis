"""Realtime endpoint helper command."""

from urllib.parse import urlencode

import click

from openai_cli.core.output import print_json

REALTIME_MODELS = [
    "gpt-realtime-2.1",
    "gpt-realtime-2.1-mini",
    "gpt-realtime-2",
    "gpt-realtime",
    "gpt-realtime-mini",
]

REALTIME_VOICES = [
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "sage",
    "shimmer",
    "verse",
    "marin",
    "cedar",
]


@click.command()
@click.option(
    "-m",
    "--model",
    type=click.Choice(REALTIME_MODELS),
    default="gpt-realtime-2.1",
    show_default=True,
    help="Realtime model to connect to. Use gpt-realtime-2.1 for best quality.",
)
@click.option(
    "--voice",
    type=click.Choice(REALTIME_VOICES),
    default="alloy",
    show_default=True,
    help="Output voice selected when the connection is established.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw connection metadata as JSON.")
def realtime(model: str, voice: str, output_json: bool) -> None:
    """Show WebSocket connection details for `/v1/realtime`."""
    url = f"wss://api.acedata.cloud/v1/realtime?{urlencode({'model': model, 'voice': voice})}"
    data = {
        "url": url,
        "model": model,
        "voice": voice,
        "protocol": "websocket",
        "authentication": "Authorization: ******",
    }

    if output_json:
        print_json(data)
        return

    click.echo(f"Realtime WebSocket URL: {url}")
    click.echo("Authenticate with: Authorization: ******")

import click

from qwen_image_cli.core.output import print_models


@click.command()
def models() -> None:
    """List available models."""
    print_models()

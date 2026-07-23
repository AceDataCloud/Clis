#!/usr/bin/env python3
"""
Recaptcha CLI - reCAPTCHA verification via AceDataCloud API.

A command-line tool for reCAPTCHA recognition and token generation
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from recaptcha_cli.commands.captcha import recognize, token, token3
from recaptcha_cli.commands.info import config

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("recaptcha-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="recaptcha-cli")
@click.option(
    "--token",
    "api_token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, api_token: str | None) -> None:
    """Recaptcha CLI - reCAPTCHA verification powered by AceDataCloud.

    Recognize captcha images and retrieve bypass tokens from the command line.

    Get your API token at https://platform.acedata.cloud

    \\b
    Examples:
      recaptcha recognize /9j/4AAQ... "/m/0k4j"
      recaptcha token 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com
      recaptcha token3 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI https://example.com login

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = api_token


# Register commands
cli.add_command(recognize)
cli.add_command(token)
cli.add_command(token3)
cli.add_command(config)


if __name__ == "__main__":
    cli()

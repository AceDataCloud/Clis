"""Music generation commands."""

import click

from adc_cli.core.client import get_client
from adc_cli.core.exceptions import AdcError
from adc_cli.core.output import print_error, print_json, print_result


@click.command()
@click.argument("prompt")
@click.option("--instrumental", is_flag=True, default=False, help="Generate instrumental only.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def music(
    ctx: click.Context,
    prompt: str,
    instrumental: bool,
    output_json: bool,
) -> None:
    """Generate music using Suno AI.

    PROMPT describes the music to generate.

    \b
    Examples:
      adc music "An upbeat electronic dance track"
      adc music "Calm piano jazz" --instrumental
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "action": "generate",
            "prompt": prompt,
            "instrumental": instrumental,
        }

        result = client.suno_music(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_result(result, "Music Result")
    except AdcError as e:
        print_error(e.message)
        raise SystemExit(1) from e

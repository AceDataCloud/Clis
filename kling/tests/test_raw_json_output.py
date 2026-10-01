"""JSON mode is machine-readable even for long prompts and media URLs."""

import json

from kling_cli.core.output import print_json


def test_json_output_preserves_long_values_and_literal_markup(capsys):
    result = {
        "prompt": "[red]海浪[/red] " * 40,
        "video_url": "https://platform2.cdn.acedata.cloud/kling/" + "a" * 120 + ".mp4",
        "cost": {"amount": 3.065328, "currency": "credit"},
    }
    print_json(result)
    assert json.loads(capsys.readouterr().out) == result

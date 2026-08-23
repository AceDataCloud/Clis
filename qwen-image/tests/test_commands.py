import json

import respx
from click.testing import CliRunner
from httpx import Response

from qwen_image_cli.main import cli


def test_generate_payload() -> None:
    with respx.mock:
        route = respx.post("https://api.acedata.cloud/qwen-image/images").mock(
            return_value=Response(200, json={"task_id": "t"})
        )
        r = CliRunner().invoke(
            cli,
            [
                "--token",
                "x",
                "generate",
                "cat",
                "--model",
                "qwen-image-3.0-pro",
                "-n",
                "2",
                "--json",
            ],
        )
        assert r.exit_code == 0
        body = json.loads(route.calls[0].request.content)
        assert body["model"] == "qwen-image-3.0-pro" and body["n"] == 2


def test_edit_caps_references() -> None:
    r = CliRunner().invoke(
        cli, ["--token", "x", "edit", "restyle", "-i", "a", "-i", "b", "-i", "c", "-i", "d"]
    )
    assert r.exit_code != 0

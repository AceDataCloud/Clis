import json

import httpx
import pytest
import respx
from click.testing import CliRunner

from kling_cli.main import cli


@pytest.mark.parametrize(
    "command,path,body",
    [
        ("elements", "/kling/elements", {"action": "presets", "page_num": 2}),
        (
            "voices",
            "/kling/voices",
            {
                "action": "create",
                "voice_name": "Narrator",
                "voice_url": "https://example.com/v.mp3",
            },
        ),
        (
            "asset-video",
            "/kling/videos",
            {
                "model": "kling-v2-6",
                "mode": "pro",
                "generate_audio": True,
                "prompt": "Hello <<<voice_1>>>",
                "voice_list": [{"voice_id": "owned-platform-id"}],
            },
        ),
    ],
)
@respx.mock
def test_asset_request_routes(command, path, body, tmp_path):
    route = respx.post("https://api.acedata.cloud" + path).mock(
        return_value=httpx.Response(200, json={"task_id": "platform"})
    )
    p = tmp_path / "request.json"
    p.write_text(json.dumps(body))
    result = CliRunner().invoke(cli, ["--token", "test", command, "--request-file", str(p)])
    assert result.exit_code == 0, result.output
    actual = json.loads(route.calls[0].request.content)
    for key, value in body.items():
        assert actual[key] == value


@respx.mock
def test_unpriced_element_creation_not_submitted(tmp_path):
    p = tmp_path / "request.json"
    p.write_text('{"action":"create"}')
    result = CliRunner().invoke(cli, ["--token", "test", "elements", "--request-file", str(p)])
    assert result.exit_code != 0
    assert len(respx.calls) == 0

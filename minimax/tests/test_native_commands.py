import json

import httpx
import pytest
import respx
from click.testing import CliRunner

from minimax_cli.main import cli


@pytest.mark.parametrize(
    "command,path,body",
    [
        (
            "max-video",
            "/minimax/videos",
            {"content": [{"type": "text", "text": "ocean"}], "resolution": "480P", "async": False},
        ),
        (
            "enhance-prompt",
            "/minimax/prompt-enhancement",
            {"content": [{"type": "text", "text": "ocean"}]},
        ),
        (
            "regenerate",
            "/minimax/regenerate",
            {"source_task_id": "owned-platform-id", "aigc_watermark": False},
        ),
        (
            "regenerate",
            "/minimax/regenerate",
            {
                "content": [
                    {"type": "text", "text": "original"},
                    {
                        "type": "video_url",
                        "role": "base_video",
                        "video_url": {"url": "https://example.com/v.mp4"},
                    },
                ]
            },
        ),
    ],
)
@respx.mock
def test_native_exact_routes(command, path, body, tmp_path):
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
def test_max_never_sends_unsupported_2k(tmp_path):
    p = tmp_path / "request.json"
    p.write_text(json.dumps({"resolution": "2K", "content": [{"type": "text", "text": "ocean"}]}))
    result = CliRunner().invoke(cli, ["--token", "test", "max-video", "--request-file", str(p)])
    assert result.exit_code != 0
    assert len(respx.calls) == 0

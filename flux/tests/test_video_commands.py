import json

import httpx
import pytest
import respx
from click.testing import CliRunner

from flux_cli.main import cli


@pytest.mark.parametrize(
    "command,path,body",
    [
        (
            "video",
            "/flux/videos",
            {
                "mode": "t2v",
                "prompt": "ocean",
                "generate_audio": False,
                "draft": False,
                "async": False,
            },
        ),
        ("video", "/flux/videos", {"mode": "draft_enhance", "draft_task_id": "owned-platform-id"}),
        (
            "video-edit",
            "/flux/video-edit",
            {"video": "https://example.com/v.mp4", "prompt": "edit"},
        ),
        (
            "video-upscale",
            "/flux/video-upscale",
            {"input_video": "https://example.com/v.mp4", "creativity": 0},
        ),
    ],
)
@respx.mock
def test_video_commands_capture_exact_request(command, path, body, tmp_path):
    route = respx.post("https://api.acedata.cloud" + path).mock(
        return_value=httpx.Response(200, json={"task_id": "platform"})
    )
    request_file = tmp_path / "request.json"
    request_file.write_text(json.dumps(body))
    result = CliRunner().invoke(
        cli, ["--token", "test", command, "--request-file", str(request_file)]
    )
    assert result.exit_code == 0, result.output
    assert "platform" in result.output
    actual = json.loads(route.calls[0].request.content)
    for key, value in body.items():
        assert actual[key] == value


@respx.mock
def test_invalid_private_draft_never_dispatches(tmp_path):
    request_file = tmp_path / "request.json"
    request_file.write_text(json.dumps({"mode": "draft_enhance", "cache_reference": "secret"}))
    result = CliRunner().invoke(
        cli, ["--token", "test", "video", "--request-file", str(request_file)]
    )
    assert result.exit_code != 0
    assert len(respx.calls) == 0

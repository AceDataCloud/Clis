import json

import httpx
import pytest
import respx
from click.testing import CliRunner

from kling_cli.main import cli


@pytest.mark.parametrize(
    "command,path,body",
    [
        ("turbo", "/kling/videos", {"prompt": "ocean", "duration": 7}),
        (
            "storyboard",
            "/kling/videos",
            {
                "shot_type": "customize",
                "duration": 5,
                "multi_prompt": [
                    {"index": 1, "prompt": "ocean", "duration": 2},
                    {"index": 2, "prompt": "beach", "duration": 3},
                ],
            },
        ),
        (
            "goods-studio",
            "/kling/goods-studio",
            {
                "contents": [
                    {"type": "ref_image", "url": "https://example.com/p.png"},
                    {"type": "goods_title", "text": "shirt"},
                ],
                "settings": {"aspect_ratio": "1:1", "duration": 15},
            },
        ),
        (
            "video-commerce",
            "/kling/video-commerce",
            {
                "contents": [
                    {"type": "avatar_id", "text": "avatar_anna_female"},
                    {"type": "speech_script", "text": "Hello"},
                ],
                "settings": {"bgm_enabled": False},
            },
        ),
    ],
)
@respx.mock
def test_native_requests(command, path, body, tmp_path):
    route = respx.post("https://api.acedata.cloud" + path).mock(
        return_value=httpx.Response(200, json={"task_id": "platform"})
    )
    p = tmp_path / "request.json"
    p.write_text(json.dumps(body))
    result = CliRunner().invoke(cli, ["--token", "test", command, "--request-file", str(p)])
    assert result.exit_code == 0, result.output
    actual = json.loads(route.calls[0].request.content)
    for key, value in body.items():
        if key == "settings":
            for k, v in value.items():
                assert actual[key][k] == v
        else:
            assert actual[key] == value


@respx.mock
def test_turbo_audio_off_rejected_before_submission(tmp_path):
    p = tmp_path / "request.json"
    p.write_text(json.dumps({"prompt": "ocean", "generate_audio": False}))
    result = CliRunner().invoke(cli, ["--token", "test", "turbo", "--request-file", str(p)])
    assert result.exit_code != 0
    assert len(respx.calls) == 0


@pytest.mark.parametrize("command", ["apparel", "virtual-try-on", "elements", "voices"])
def test_unpublished_commands_are_not_discoverable(command):
    result = CliRunner().invoke(cli, ["--token", "test", command, "--help"])
    assert result.exit_code != 0
    assert "No such command" in result.output

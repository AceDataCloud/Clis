"""Exercise the two native media protocols through the installed command group."""

import json
from unittest.mock import patch

import httpx
import pytest
import respx
from click.testing import CliRunner

from adc_cli.main import cli

BASE = "https://api.acedata.cloud"


def run(*args):
    return CliRunner().invoke(cli, ["--token", "fixture-token", *args])


@pytest.mark.parametrize("alias", ["gpt-image", "openai"])
@pytest.mark.parametrize(
    "field,value", [("url", "https://example.com/result.png"), ("b64_json", "YWJjZA==")]
)
@respx.mock
def test_gpt_sync_preserves_model_and_delivered_field(alias, field, value):
    response = {"created": 12345, "data": [{field: value}]}
    route = respx.post(BASE + "/openai/images/generations").mock(
        return_value=httpx.Response(200, json=response)
    )
    result = run(
        "image",
        "fox",
        "--service",
        alias,
        "-m",
        "gpt-image-2:official",
        "-s",
        "1536x1024",
        "-n",
        "2",
        "--response-format",
        field,
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == response
    assert json.loads(route.calls.last.request.content) == {
        "prompt": "fox",
        "model": "gpt-image-2:official",
        "n": 2,
        "size": "1536x1024",
        "response_format": field,
    }


@respx.mock
def test_gpt_edit_and_async_have_their_own_contract():
    route = respx.post(BASE + "/openai/images/edits").mock(
        return_value=httpx.Response(200, json={"task_id": "image42"})
    )
    result = run(
        "image",
        "add snow",
        "--service",
        "gpt-image",
        "--model",
        "future-user-model",
        "--image-url",
        "https://example.com/ref.png",
        "--async",
    )
    assert result.exit_code == 0 and result.output.strip() == "Task ID: image42"
    assert json.loads(route.calls.last.request.content) == {
        "prompt": "add snow",
        "model": "future-user-model",
        "image": "https://example.com/ref.png",
        "async": True,
    }


@pytest.mark.parametrize(
    "extra,action",
    [([], "text2video"), (["--image-url", "https://example.com/frame.jpg"], "image2video")],
)
@respx.mock
def test_kling_submits_native_actions_and_exact_model(extra, action):
    answer = {"task_id": "k42", "state": "pending"}
    route = respx.post(BASE + "/kling/videos").mock(return_value=httpx.Response(200, json=answer))
    result = run(
        "video",
        "pan left",
        "--service",
        "kling",
        "-m",
        "kling-v3",
        "--mode",
        "pro",
        "--duration",
        "5",
        "--aspect-ratio",
        "16:9",
        "--json",
        *extra,
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == answer
    body = {
        "action": action,
        "prompt": "pan left",
        "model": "kling-v3",
        "mode": "pro",
        "duration": 5,
        "aspect_ratio": "16:9",
        "async": True,
    }
    if extra:
        body["start_image_url"] = extra[1]
    assert json.loads(route.calls.last.request.content) == body


@pytest.mark.parametrize(
    "service,path,output",
    [
        ("gpt-image", "openai", {"created": 42, "data": [{"b64_json": "YWJjZA=="}]}),
        ("openai", "openai", {"created": 42, "data": [{"url": "https://example.com/result.png"}]}),
        ("kling", "kling", {"success": True, "video_url": "https://example.com/output.mp4"}),
    ],
)
@respx.mock
def test_task_and_wait_preserve_nested_delivery(service, path, output):
    found = {"id": "42", "finished_at": "2026-11-27T18:00:00Z", "response": output}
    queued = {"id": "42", "response": {"state": "processing"}, "finished_at": None}
    route = respx.post(f"{BASE}/{path}/tasks").mock(
        side_effect=[httpx.Response(200, json=r) for r in (found, queued, found)]
    )
    assert json.loads(run("task", "42", "-s", service).output) == found
    with patch("adc_cli.commands.task.time.sleep"):
        waited = run("wait", "42", "-s", service, "--interval", "1", "--json")
    assert waited.exit_code == 0 and json.loads(waited.output) == found
    assert len(route.calls) == 3
    assert all(
        json.loads(call.request.content) == {"action": "retrieve", "id": "42"}
        for call in route.calls
    )


@pytest.mark.parametrize(
    "output", [{"success": False, "error": {"message": "upstream failure"}}, {"data": []}]
)
@respx.mock
def test_finished_tasks_without_delivery_exit_nonzero(output):
    record = {"id": "42", "finished_at": "2026-11-27T18:00:00Z", "response": output}
    respx.post(BASE + "/openai/tasks").mock(return_value=httpx.Response(200, json=record))
    result = run("wait", "42", "-s", "gpt-image", "--json")
    assert result.exit_code == 1 and json.loads(result.stdout) == record


def test_service_only_options_fail_before_transport():
    assert run("image", "fox", "--service", "gpt-image").exit_code == 2
    assert run("video", "pan", "--service", "kling", "--loop").exit_code == 2
    assert run("video", "pan", "--service", "seedance", "--mode", "pro").exit_code == 2


@pytest.mark.parametrize(
    "reply", [{}, {"id": "different-job", "finished_at": "2026-11-27T18:00:00Z"}]
)
@respx.mock
def test_lookup_does_not_report_a_missing_or_different_task_as_success(reply):
    respx.post(BASE + "/kling/tasks").mock(return_value=httpx.Response(200, json=reply))
    result = run("task", "42", "--service", "kling")
    assert result.exit_code == 1 and "No matching task" in result.output

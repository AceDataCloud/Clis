"""Native Messages CLI requests preserve explicit models and authentication."""

import json

import pytest
import respx
from click.testing import CliRunner

from aichat_cli.core.config import settings
from aichat_cli.main import cli


@pytest.fixture(autouse=True)
def api_base(monkeypatch):
    monkeypatch.setattr(settings, "api_base_url", "https://api.acedata.cloud")


@respx.mock
@pytest.mark.parametrize("model", ["claude-sonnet-5-5", "claude-opus-5-5", "future-messages-model"])
def test_native_messages_model_and_body(model):
    route = respx.post("https://api.acedata.cloud/v1/messages").respond(
        200,
        json={
            "type": "message",
            "model": model,
            "content": [{"type": "text", "text": "Fixture reply"}],
        },
    )
    result = CliRunner().invoke(
        cli,
        [
            "--token",
            "synthetic-token",
            "messages",
            "Hello",
            "--model",
            model,
            "--max-tokens",
            "12",
            "--system",
            "Be brief",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Fixture reply" in result.output
    assert len(route.calls) == 1
    request = route.calls[0].request
    assert request.headers["authorization"] == "Bearer synthetic-token"
    assert "x-api-key" not in request.headers
    assert json.loads(request.content) == {
        "model": model,
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 12,
        "system": "Be brief",
    }


@respx.mock
def test_native_messages_preserves_tool_response():
    native = {
        "type": "message",
        "content": [{"type": "tool_use", "id": "fixture", "name": "test", "input": {}}],
    }
    respx.post("https://api.acedata.cloud/v1/messages").respond(200, json=native)
    result = CliRunner().invoke(
        cli,
        ["--token", "synthetic-token", "messages", "Hello", "-m", "claude-sonnet-5-5", "--json"],
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == native


@respx.mock
@pytest.mark.parametrize("args", [[], ["--model", ""], ["--model", "model", "--max-tokens", "0"]])
def test_invalid_parameters_make_no_request(args):
    result = CliRunner().invoke(cli, ["--token", "synthetic-token", "messages", "Hello", *args])
    assert result.exit_code == 2
    assert not respx.calls


@respx.mock
def test_rejected_model_does_not_fall_back():
    route = respx.post("https://api.acedata.cloud/v1/messages").respond(
        403, json={"error": {"message": "denied"}}
    )
    result = CliRunner().invoke(
        cli, ["--token", "synthetic-token", "messages", "Hello", "-m", "claude-sonnet-5-5"]
    )
    assert result.exit_code == 1
    assert len(route.calls) == 1
    assert len(respx.calls) == 1

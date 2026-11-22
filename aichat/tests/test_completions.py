"""Unified Chat Completions keeps new model IDs and their requested wire shape."""

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
@pytest.mark.parametrize(
    "model", ["kimi-k2.7-code", "gemini-4-argon", "gpt-4o-image", "future-chat-model"]
)
def test_unified_models_are_not_restricted_by_legacy_suggestions(model):
    route = respx.post("https://api.acedata.cloud/v1/chat/completions").respond(
        200, json={"choices": [{"message": {"content": "Fixture reply"}}]}
    )
    result = CliRunner().invoke(
        cli, ["--token", "synthetic-token", "completions", "Hello", "--model", model]
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
    }


@respx.mock
def test_explicit_options_and_full_json_are_preserved():
    native = {"choices": [{"message": {"content": None, "tool_calls": [{"id": "fixture"}]}}]}
    route = respx.post("https://api.acedata.cloud/v1/chat/completions").respond(200, json=native)
    result = CliRunner().invoke(
        cli,
        [
            "--token",
            "synthetic-token",
            "completions",
            "Hello",
            "-m",
            "gpt-5-pro",
            "--system",
            "Be brief",
            "--max-completion-tokens",
            "12",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == native
    assert json.loads(route.calls[0].request.content) == {
        "model": "gpt-5-pro",
        "messages": [
            {"role": "system", "content": "Be brief"},
            {"role": "user", "content": "Hello"},
        ],
        "max_completion_tokens": 12,
    }


@respx.mock
@pytest.mark.parametrize(
    "args", [[], ["--model", ""], ["--model", "model", "--max-completion-tokens", "0"]]
)
def test_invalid_arguments_make_no_request(args):
    result = CliRunner().invoke(cli, ["--token", "synthetic-token", "completions", "Hello", *args])
    assert result.exit_code == 2
    assert not respx.calls


@respx.mock
def test_rejection_never_switches_to_messages():
    route = respx.post("https://api.acedata.cloud/v1/chat/completions").respond(
        400, json={"error": {"message": "unsupported protocol"}}
    )
    result = CliRunner().invoke(
        cli, ["--token", "synthetic-token", "completions", "Hello", "-m", "claude-sonnet-5-5"]
    )
    assert result.exit_code == 1
    assert len(route.calls) == 1
    assert len(respx.calls) == 1

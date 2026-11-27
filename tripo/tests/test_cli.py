from unittest.mock import patch

import httpx
from click.testing import CliRunner

from tripo_cli.main import cli


def test_generation_and_same_key():
    with patch(
        "tripo_cli.main.httpx.post",
        return_value=httpx.Response(
            200,
            request=httpx.Request("POST", "https://api.acedata.cloud"),
            json={"task_id": "t"},
        ),
    ) as call:
        result = CliRunner().invoke(
            cli,
            [
                "--token",
                "token",
                "generate",
                "--json",
                '{"prompt":"chair"}',
                "--idempotency-key",
                "retry",
            ],
        )
    assert result.exit_code == 0
    assert call.call_args.args[0].endswith("/tripo/generations")
    assert call.call_args.kwargs["headers"]["Idempotency-Key"] == "retry"
    assert call.call_args.kwargs["json"] == {"prompt": "chair", "async": True}


def test_batch_and_operation_input():
    with patch("tripo_cli.main.post") as call:
        assert CliRunner().invoke(cli, ["tasks", "--trace", "a", "b"]).exit_code == 0
        call.assert_called_with(
            "tasks", {"action": "retrieve_batch", "trace_ids": ["a", "b"]}
        )
        assert (
            CliRunner()
            .invoke(
                cli, ["models", "convert", "--json", '{"model_id":"x","format":"FBX"}']
            )
            .exit_code
            == 0
        )
        call.assert_called_with(
            "models",
            {"model_id": "x", "format": "FBX", "action": "convert", "async": True},
            None,
        )
        assert (
            CliRunner()
            .invoke(cli, ["animations", "rig", "--json", '{"action":"retarget"}'])
            .exit_code
            != 0
        )

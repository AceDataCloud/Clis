"""Offline CLI contract checks."""

import json
from unittest.mock import Mock, patch

import httpx
import pytest
import respx
from click.testing import CliRunner

from acemusic_cli.commands.task import task_state
from acemusic_cli.core.client import AceMusicClient
from acemusic_cli.core.exceptions import AceMusicTimeoutError
from acemusic_cli.main import cli


def test_idea_and_custom_wire_payload(tmp_path):
    runner = CliRunner()
    client = Mock()
    client.generate_audio.return_value = {"task_id": "one"}
    with patch("acemusic_cli.commands.music.get_client", return_value=client):
        result = runner.invoke(cli, ["generate", "warm folk"])
        assert result.exit_code == 0, result.output
        assert client.generate_audio.call_args.kwargs == {
            "action": "generate",
            "model": "acemusic-v1.1",
            "custom": False,
            "async": True,
            "prompt": "warm folk",
        }
        p = tmp_path / "lyrics.txt"
        p.write_text("[Verse] Home")
        result = runner.invoke(
            cli, ["generate", "--lyric-file", str(p), "--style", "folk", "--title", "Home"]
        )
        assert result.exit_code == 0, result.output
        assert client.generate_audio.call_args.kwargs["lyric"] == "[Verse] Home"
        assert "lyrics" not in client.generate_audio.call_args.kwargs
        assert runner.invoke(cli, ["generate", "--lyric-file", str(p)]).exit_code != 0


@respx.mock
def test_paid_timeout_is_not_retried():
    route = respx.post("https://api.acedata.cloud/acemusic/audios").mock(
        side_effect=httpx.ReadTimeout("lost")
    )
    with pytest.raises(AceMusicTimeoutError):
        AceMusicClient(api_token="token").generate_audio(prompt="folk")
    assert route.call_count == 1
    assert json.loads(route.calls[0].request.content)["async"] is True


def test_wait_partial_failure_terminates_without_generation():
    client = Mock()
    client.query_task.return_value = {
        "id": "one",
        "state": "partial_failed",
        "response": {
            "success": False,
            "data": [{"audio_url": "https://cdn.acedata.cloud/one.mp3"}],
        },
    }
    with patch("acemusic_cli.commands.task.get_client", return_value=client):
        result = CliRunner().invoke(cli, ["wait", "one"])
        assert result.exit_code == 1
        client.query_task.assert_called_once_with(action="retrieve", id="one")
        client.generate_audio.assert_not_called()
    assert (
        task_state({"state": "processing", "response": {"data": [{"audio_url": "preview"}]}})
        == "processing"
    )


def test_models_is_free():
    result = CliRunner().invoke(cli, ["models"])
    assert result.exit_code == 0 and "acemusic-v1.1" in result.output


@pytest.mark.parametrize("title_args", [[], ["--title", ""], ["--title", "   "]])
def test_custom_requires_title_before_contacting_api(tmp_path, title_args):
    lyric_file = tmp_path / "lyrics.txt"
    lyric_file.write_text("[Verse] Home")
    with patch("acemusic_cli.commands.music.get_client") as get_client:
        result = CliRunner().invoke(
            cli, ["generate", "--lyric-file", str(lyric_file), "--style", "folk", *title_args]
        )
    assert result.exit_code == 2
    assert "--title" in result.output
    get_client.assert_not_called()


def test_reference_commands_send_once_with_public_ids(tmp_path):
    lyric_file = tmp_path / "lyrics.txt"
    lyric_file.write_text("[Verse] Original home")
    client = Mock()
    client.generate_audio.return_value = {"task_id": "one"}
    runner = CliRunner()
    with patch("acemusic_cli.commands.music.get_client", return_value=client):
        result = runner.invoke(
            cli, ["upload", "https://example.com/owned.mp3", "--audio-id", "anchor"]
        )
        assert result.exit_code == 0, result.output
        assert client.generate_audio.call_args.kwargs == {
            "action": "upload",
            "audio_url": "https://example.com/owned.mp3",
            "audio_id": "anchor",
            "async": True,
        }
        result = runner.invoke(
            cli, ["cover", "audio-a", "--lyric-file", str(lyric_file), "--style", "folk"]
        )
        assert result.exit_code == 0, result.output
        payload = client.generate_audio.call_args.kwargs
        assert payload["action"] == "cover" and payload["audio_id"] == "audio-a"
        assert payload["audio_influence"] == 60 and payload["model"] == "acemusic-v1.1"
        assert "title" not in payload and "custom" not in payload
        result = runner.invoke(
            cli,
            ["mashup", "audio-a", "audio-b", "--lyric-file", str(lyric_file), "--style", "folk"],
        )
        assert result.exit_code == 0, result.output
        assert client.generate_audio.call_args.kwargs["mashup_audio_ids"] == ["audio-a", "audio-b"]
        assert client.generate_audio.call_count == 3


def test_invalid_reference_commands_never_contact_api(tmp_path):
    lyric_file = tmp_path / "lyrics.txt"
    lyric_file.write_text("[Verse] Original home")
    with patch("acemusic_cli.commands.music.get_client") as get_client:
        runner = CliRunner()
        for args in [
            ["upload", "http://example.com/owned.mp3"],
            [
                "cover",
                "a",
                "--lyric-file",
                str(lyric_file),
                "--style",
                "folk",
                "--audio-influence",
                "nan",
            ],
            [
                "cover",
                "a",
                "--lyric-file",
                str(lyric_file),
                "--style",
                "folk",
                "--audio-influence",
                "101",
            ],
            ["mashup", "a", "a", "--lyric-file", str(lyric_file), "--style", "folk"],
        ]:
            assert runner.invoke(cli, args).exit_code == 2
        get_client.assert_not_called()

import json

import httpx
import pytest
import respx
from click.testing import CliRunner

from suno_cli.main import cli


@pytest.mark.parametrize(
    "option,value", [(None, None), ("--personalization", True), ("--no-personalization", False)]
)
@pytest.mark.parametrize("custom", [False, True])
@respx.mock
def test_personalization_request(option, value, custom, mock_audio_response):
    runner = CliRunner()
    route = respx.post("https://api.acedata.cloud/suno/audios").mock(
        return_value=httpx.Response(200, json=mock_audio_response)
    )
    args = (
        ["--token", "test", "custom", "--lyric", "lyrics", "--title", "title", "--style", "pop"]
        if custom
        else ["--token", "test", "generate", "pop"]
    )
    if option:
        args.append(option)
    result = runner.invoke(cli, args + ["--json"])
    assert result.exit_code == 0, result.output
    body = json.loads(route.calls[0].request.content)
    assert ("personalization" in body) is (value is not None)
    if value is not None:
        assert body["personalization"] is value
    assert "use_personalization" not in body

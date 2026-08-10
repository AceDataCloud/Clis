"""Tests for Face Change CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from face_change_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def ok() -> dict[str, object]:
    return {"task_id": "task-123", "state": "succeeded"}


class TestGlobalCommands:
    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        for command in ["analyze", "beautify", "change-age", "change-gender", "detect-live", "swap", "cartoon"]:
            assert command in result.output


class TestFaceCommands:
    @respx.mock
    def test_analyze_payload(self, runner):
        route = respx.post("https://api.acedata.cloud/face/analyze").mock(return_value=Response(200, json=ok()))
        result = runner.invoke(cli, ["--token", "test-token", "analyze", "https://e.test/face.jpg", "--mode", "1", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent == {"image_url": "https://e.test/face.jpg", "mode": 1.0}

    @respx.mock
    def test_beautify_payload(self, runner):
        route = respx.post("https://api.acedata.cloud/face/beautify").mock(return_value=Response(200, json=ok()))
        result = runner.invoke(cli, ["--token", "test-token", "beautify", "https://e.test/face.jpg", "--smoothing", "0.6", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["image_url"] == "https://e.test/face.jpg"
        assert sent["smoothing"] == 0.6

    @respx.mock
    def test_change_age_payload(self, runner):
        route = respx.post("https://api.acedata.cloud/face/change-age").mock(return_value=Response(200, json=ok()))
        result = runner.invoke(cli, ["--token", "test-token", "change-age", "https://e.test/face.jpg", "--age-infos", '[{"age":30}]', "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["age_infos"] == [{"age": 30}]

    @respx.mock
    def test_change_gender_payload(self, runner):
        route = respx.post("https://api.acedata.cloud/face/change-gender").mock(return_value=Response(200, json=ok()))
        result = runner.invoke(cli, ["--token", "test-token", "change-gender", "https://e.test/face.jpg", "--gender-infos", '[{"gender":"male"}]', "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["gender_infos"] == [{"gender": "male"}]

    @respx.mock
    def test_detect_live_payload(self, runner):
        route = respx.post("https://api.acedata.cloud/face/detect-live").mock(return_value=Response(200, json=ok()))
        result = runner.invoke(cli, ["--token", "test-token", "detect-live", "https://e.test/face.jpg", "--face-model-version", "2", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["face_model_version"] == 2.0

    @respx.mock
    def test_swap_payload(self, runner):
        route = respx.post("https://api.acedata.cloud/face/swap").mock(return_value=Response(200, json=ok()))
        result = runner.invoke(cli, ["--token", "test-token", "swap", "--source-image-url", "https://e.test/source.jpg", "--target-image-url", "https://e.test/target.jpg", "--async", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["source_image_url"] == "https://e.test/source.jpg"
        assert sent["target_image_url"] == "https://e.test/target.jpg"
        assert sent["async"] is True

    @respx.mock
    def test_cartoon_payload(self, runner):
        route = respx.post("https://api.acedata.cloud/face/cartoon").mock(return_value=Response(200, json=ok()))
        result = runner.invoke(cli, ["--token", "test-token", "cartoon", "https://e.test/face.jpg", "--json"])
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent == {"image_url": "https://e.test/face.jpg"}

"""Tests for Kickart CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from kickart_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "kickart-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "video" in result.output
        assert "viral-video" in result.output
        assert "template-video" in result.output
        assert "config" in result.output

    def test_help_video(self, runner):
        result = runner.invoke(cli, ["video", "--help"])
        assert result.exit_code == 0
        assert "--duration" in result.output
        assert "--mode" in result.output
        assert "--async" in result.output

    def test_help_viral_video(self, runner):
        result = runner.invoke(cli, ["viral-video", "--help"])
        assert result.exit_code == 0
        assert "--ref-video" in result.output
        assert "--language" in result.output
        assert "--async" in result.output

    def test_help_template_video(self, runner):
        result = runner.invoke(cli, ["template-video", "--help"])
        assert result.exit_code == 0
        assert "--template-id" in result.output
        assert "--resource" in result.output
        assert "--async" in result.output


class TestVideoCommand:
    """Tests for e-commerce video generation command."""

    @respx.mock
    def test_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kickart/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "video",
                "--duration",
                "15",
                "--product-url",
                "https://example.com/product",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "3a8b1c2d-4e5f-6789-abcd-ef0123456789"

    @respx.mock
    def test_video_sends_correct_payload(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kickart/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "video",
                "--duration",
                "30",
                "--mode",
                "pro",
                "--aspect-ratio",
                "16:9",
                "--language",
                "en",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["duration"] == 30
        assert sent["mode"] == "pro"
        assert sent["aspect_ratio"] == "16:9"
        assert sent["language"] == "en"
        assert "async" not in sent

    @respx.mock
    def test_video_async(self, runner, mock_video_async_response):
        route = respx.post("https://api.acedata.cloud/kickart/videos").mock(
            return_value=Response(200, json=mock_video_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "video",
                "--duration",
                "15",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_video_with_user_images(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kickart/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "video",
                "--duration",
                "15",
                "--user-images",
                '["https://example.com/img1.jpg"]',
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["user_images"] == ["https://example.com/img1.jpg"]

    def test_video_missing_duration(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "video"])
        assert result.exit_code != 0

    def test_video_invalid_duration(self, runner):
        result = runner.invoke(
            cli, ["--token", "test-token", "video", "--duration", "20"]
        )
        assert result.exit_code != 0

    def test_video_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "video", "--duration", "15"])
        assert result.exit_code != 0


class TestViralVideoCommand:
    """Tests for viral video generation command."""

    @respx.mock
    def test_viral_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kickart/viral-videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "viral-video",
                "--ref-video",
                "https://example.com/ref.mp4",
                "--language",
                "en",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "3a8b1c2d-4e5f-6789-abcd-ef0123456789"

    @respx.mock
    def test_viral_video_sends_correct_payload(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kickart/viral-videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "viral-video",
                "--ref-video",
                "https://example.com/ref.mp4",
                "--language",
                "zh",
                "--mode",
                "advanced",
                "--similarity",
                "high",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["ref_video"] == "https://example.com/ref.mp4"
        assert sent["language"] == "zh"
        assert sent["mode"] == "advanced"
        assert sent["similarity"] == "high"
        assert "async" not in sent

    @respx.mock
    def test_viral_video_async(self, runner, mock_video_async_response):
        route = respx.post("https://api.acedata.cloud/kickart/viral-videos").mock(
            return_value=Response(200, json=mock_video_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "viral-video",
                "--ref-video",
                "https://example.com/ref.mp4",
                "--language",
                "en",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_viral_video_missing_ref_video(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "viral-video", "--language", "en"])
        assert result.exit_code != 0

    def test_viral_video_missing_language(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "viral-video", "--ref-video", "https://example.com/ref.mp4"],
        )
        assert result.exit_code != 0


class TestTemplateVideoCommand:
    """Tests for template video generation command."""

    @respx.mock
    def test_template_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kickart/template-videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "template-video",
                "--template-id",
                "tmpl_123",
                "--resource",
                '[{"type":"image","url":"https://example.com/img.jpg"}]',
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "3a8b1c2d-4e5f-6789-abcd-ef0123456789"

    @respx.mock
    def test_template_video_sends_correct_payload(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kickart/template-videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "template-video",
                "--template-id",
                "tmpl_456",
                "--resource",
                '[{"type":"video","url":"https://example.com/vid.mp4"}]',
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["template_id"] == "tmpl_456"
        assert sent["resource_list"] == [{"type": "video", "url": "https://example.com/vid.mp4"}]
        assert "async" not in sent

    @respx.mock
    def test_template_video_async(self, runner, mock_video_async_response):
        route = respx.post("https://api.acedata.cloud/kickart/template-videos").mock(
            return_value=Response(200, json=mock_video_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "template-video",
                "--template-id",
                "tmpl_123",
                "--resource",
                '[{"type":"image","url":"https://example.com/img.jpg"}]',
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    def test_template_video_missing_template_id(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "template-video",
                "--resource",
                '[{"type":"image","url":"https://example.com/img.jpg"}]',
            ],
        )
        assert result.exit_code != 0

    def test_template_video_missing_resource(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "template-video", "--template-id", "tmpl_123"],
        )
        assert result.exit_code != 0

    def test_template_video_invalid_resource_json(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "template-video",
                "--template-id",
                "tmpl_123",
                "--resource",
                "not-json",
            ],
        )
        assert result.exit_code != 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

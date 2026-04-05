"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from adc_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "adc" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "image" in result.output
        assert "video" in result.output
        assert "music" in result.output
        assert "search" in result.output

    def test_help_image(self, runner):
        result = runner.invoke(cli, ["image", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--service" in result.output

    def test_help_video(self, runner):
        result = runner.invoke(cli, ["video", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--service" in result.output


# ─── Image Commands ──────────────────────────────────────────────────────


class TestImageCommands:
    """Tests for image generation commands."""

    @respx.mock
    def test_image_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "image", "A sunset", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_image_rich_output(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "image", "A sunset"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_image_midjourney(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/midjourney/imagine").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "image", "A city", "--service", "midjourney", "--json"],
        )
        assert result.exit_code == 0
        assert route.called

    @respx.mock
    def test_image_with_edit(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/flux/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image",
                "Add sunglasses",
                "--image-url",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "edit"
        assert body["model"] == "flux-kontext-pro"

    @respx.mock
    def test_image_seedream(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/seedream/images").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "image", "Logo", "--service", "seedream", "--json"],
        )
        assert result.exit_code == 0
        assert route.called

    def test_image_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "image", "test"])
        assert result.exit_code != 0


# ─── Video Commands ──────────────────────────────────────────────────────


class TestVideoCommands:
    """Tests for video generation commands."""

    @respx.mock
    def test_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/luma/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "video", "A sunset", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "test-task-789"

    @respx.mock
    def test_video_sora(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/sora/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "video", "A rocket", "--service", "sora", "--json"],
        )
        assert result.exit_code == 0
        assert route.called

    @respx.mock
    def test_video_veo(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/veo/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "video", "Clouds", "--service", "veo", "--json"],
        )
        assert result.exit_code == 0
        assert route.called

    def test_video_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "video", "test"])
        assert result.exit_code != 0


# ─── Music Commands ──────────────────────────────────────────────────────


class TestMusicCommands:
    """Tests for music generation commands."""

    @respx.mock
    def test_music_json(self, runner, mock_music_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_music_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "music", "Jazz piano", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "test-task-music"

    @respx.mock
    def test_music_instrumental(self, runner, mock_music_response):
        route = respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_music_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "music", "Ambient", "--instrumental", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["instrumental"] is True

    def test_music_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "music", "test"])
        assert result.exit_code != 0


# ─── Search Commands ─────────────────────────────────────────────────────


class TestSearchCommands:
    """Tests for search commands."""

    @respx.mock
    def test_search_json(self, runner, mock_search_response):
        respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "search", "artificial intelligence", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "organic" in data

    @respx.mock
    def test_search_with_type(self, runner, mock_search_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "search", "tech", "-t", "news", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["type"] == "news"

    @respx.mock
    def test_search_with_country(self, runner, mock_search_response):
        route = respx.post("https://api.acedata.cloud/serp/google").mock(
            return_value=Response(200, json=mock_search_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "search", "test", "-c", "uk", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["country"] == "uk"

    def test_search_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "search", "test"])
        assert result.exit_code != 0


# ─── Task Commands ────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/flux/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "task-123", "-s", "flux", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["state"] == "succeeded"

    @respx.mock
    def test_task_luma(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/luma/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "task-456", "-s", "luma", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_wait_completed(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/flux/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "wait", "task-123", "-s", "flux", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["state"] == "succeeded"


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_services(self, runner):
        result = runner.invoke(cli, ["services"])
        assert result.exit_code == 0
        assert "flux" in result.output
        assert "suno" in result.output
        assert "luma" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output


# ─── Auth Commands ─────────────────────────────────────────────────────────


class TestAuthCommands:
    """Tests for auth commands."""

    def test_auth_help(self, runner):
        result = runner.invoke(cli, ["auth", "--help"])
        assert result.exit_code == 0
        assert "login" in result.output
        assert "status" in result.output

    def test_auth_status(self, runner):
        result = runner.invoke(cli, ["auth", "status"])
        assert result.exit_code == 0
        assert "Auth Status" in result.output

    def test_auth_login(self, runner):
        from unittest.mock import patch

        with (
            patch("adc_cli.commands.auth.save_token_to_config") as mock_save,
        ):
            result = runner.invoke(cli, ["auth", "login", "--token", "my-test-token"])
            assert result.exit_code == 0
            mock_save.assert_called_once_with("my-test-token")
            assert "Token saved" in result.output

"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from kling_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "kling-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "lip-sync" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_help_motion(self, runner):
        result = runner.invoke(cli, ["motion", "--help"])
        assert result.exit_code == 0
        assert "--image-url" in result.output
        assert "--video-url" in result.output


# ─── Generate Commands ─────────────────────────────────────────────────────


class TestGenerateCommands:
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A test prompt", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_generate_rich_output(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A test prompt"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--model", "kling-v3", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "kling-v3"

    @respx.mock
    def test_generate_with_mode_4k(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--mode", "4k", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["mode"] == "4k"

    @respx.mock
    def test_generate_with_callback(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--callback-url",
                "https://example.com/callback",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_timeout(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--timeout", "600", "--json"],
        )
        assert result.exit_code == 0
        assert route.called
        assert route.calls.last.request.content
        body = json.loads(route.calls.last.request.content)
        assert body["timeout"] == 600

    @respx.mock
    def test_generate_with_async(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "generate", "test", "--async", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["async"] is True

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_image_to_video_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "--start-image-url",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_image_to_video_action(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "--start-image-url",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "image2video"

    @respx.mock
    def test_extend_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extend", "--video-id", "video-123", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_extend_action(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extend", "--video-id", "video-123", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["action"] == "extend"
        assert body["video_id"] == "video-123"

    @respx.mock
    def test_generate_with_camera_control(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--camera-control",
                '{"type": "simple", "config": {"horizontal": 0.5}}',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["camera_control"] == {"type": "simple", "config": {"horizontal": 0.5}}

    def test_generate_with_invalid_camera_control(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--camera-control",
                "not-valid-json",
            ],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_generate_with_element_ids(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--element-id",
                "elem-001",
                "--element-id",
                "elem-002",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["element_list"] == [{"element_id": "elem-001"}, {"element_id": "elem-002"}]

    @respx.mock
    def test_generate_with_video_list(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--video-list",
                '[{"video_url": "https://example.com/ref.mp4", "refer_type": "base"}]',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["video_list"] == [
            {"video_url": "https://example.com/ref.mp4", "refer_type": "base"}
        ]

    def test_generate_with_invalid_video_list(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "test",
                "--video-list",
                "not-valid-json",
            ],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_image_to_video_with_camera_control(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "--start-image-url",
                "https://example.com/photo.jpg",
                "--camera-control",
                '{"type": "down_back"}',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["camera_control"] == {"type": "down_back"}

    @respx.mock
    def test_image_to_video_with_element_ids(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "--start-image-url",
                "https://example.com/photo.jpg",
                "--element-id",
                "elem-abc",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["element_list"] == [{"element_id": "elem-abc"}]

    @respx.mock
    def test_image_to_video_with_video_list(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/kling/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "image-to-video",
                "Animate this",
                "--start-image-url",
                "https://example.com/photo.jpg",
                "--video-list",
                '[{"video_url": "https://example.com/ref.mp4", "refer_type": "feature"}]',
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["video_list"] == [
            {"video_url": "https://example.com/ref.mp4", "refer_type": "feature"}
        ]

    def test_extend_no_video_id(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "extend"])
        assert result.exit_code != 0


# ─── Motion Commands ───────────────────────────────────────────────────────


class TestMotionCommands:
    """Tests for motion generation commands."""

    @respx.mock
    def test_motion_json(self, runner, mock_motion_response):
        respx.post("https://api.acedata.cloud/kling/motion").mock(
            return_value=Response(200, json=mock_motion_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_motion_rich_output(self, runner, mock_motion_response):
        respx.post("https://api.acedata.cloud/kling/motion").mock(
            return_value=Response(200, json=mock_motion_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_motion_payload(self, runner, mock_motion_response):
        route = respx.post("https://api.acedata.cloud/kling/motion").mock(
            return_value=Response(200, json=mock_motion_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
                "--mode",
                "pro",
                "--no-keep-original-sound",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["image_url"] == "https://example.com/img.jpg"
        assert body["video_url"] == "https://example.com/ref.mp4"
        assert body["mode"] == "pro"
        assert body["keep_original_sound"] == "no"

    @respx.mock
    def test_motion_with_async(self, runner, mock_motion_response):
        route = respx.post("https://api.acedata.cloud/kling/motion").mock(
            return_value=Response(200, json=mock_motion_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
                "--async",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["async"] is True

    def test_motion_missing_image_url(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--video-url",
                "https://example.com/ref.mp4",
            ],
        )
        assert result.exit_code != 0

    def test_motion_missing_video_url(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
            ],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_motion_character_orientation_image(self, runner, mock_motion_response):
        route = respx.post("https://api.acedata.cloud/kling/motion").mock(
            return_value=Response(200, json=mock_motion_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
                "--character-orientation",
                "image",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["character_orientation"] == "image"

    @respx.mock
    def test_motion_character_orientation_video(self, runner, mock_motion_response):
        route = respx.post("https://api.acedata.cloud/kling/motion").mock(
            return_value=Response(200, json=mock_motion_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
                "--character-orientation",
                "video",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["character_orientation"] == "video"

    def test_motion_invalid_character_orientation(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
                "--character-orientation",
                "invalid-value",
            ],
        )
        assert result.exit_code != 0

    def test_motion_rejects_4k_mode(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "motion",
                "--image-url",
                "https://example.com/img.jpg",
                "--video-url",
                "https://example.com/ref.mp4",
                "--mode",
                "4k",
            ],
        )
        assert result.exit_code != 0


class TestLipSyncCommands:
    """Tests for lip-sync commands."""

    @respx.mock
    def test_lip_sync_audio_json(self, runner, mock_lip_sync_response):
        route = respx.post("https://api.acedata.cloud/kling/lip-sync").mock(
            return_value=Response(200, json=mock_lip_sync_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "lip-sync",
                "--mode",
                "audio2video",
                "--video-id",
                "video-123",
                "--audio-url",
                "https://example.com/voice.mp3",
                "--audio-type",
                "url",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "test-lip-sync-task-123"
        body = json.loads(route.calls.last.request.content)
        assert body["mode"] == "audio2video"
        assert body["video_id"] == "video-123"
        assert body["audio_url"] == "https://example.com/voice.mp3"
        assert body["audio_type"] == "url"

    @respx.mock
    def test_lip_sync_text_payload(self, runner, mock_lip_sync_response):
        route = respx.post("https://api.acedata.cloud/kling/lip-sync").mock(
            return_value=Response(200, json=mock_lip_sync_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "lip-sync",
                "--mode",
                "text2video",
                "--video-url",
                "https://example.com/video.mp4",
                "--text",
                "Hello world",
                "--voice-id",
                "voice-123",
                "--voice-language",
                "en",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["mode"] == "text2video"
        assert body["video_url"] == "https://example.com/video.mp4"
        assert body["text"] == "Hello world"
        assert body["voice_id"] == "voice-123"
        assert body["voice_language"] == "en"

    def test_lip_sync_requires_video(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "lip-sync", "--mode", "audio2video"],
        )
        assert result.exit_code != 0

    def test_lip_sync_requires_audio_for_audio_mode(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "lip-sync",
                "--mode",
                "audio2video",
                "--video-id",
                "video-123",
            ],
        )
        assert result.exit_code != 0

    def test_lip_sync_requires_text_and_voice_for_text_mode(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "lip-sync",
                "--mode",
                "text2video",
                "--video-id",
                "video-123",
                "--text",
                "Hello world",
            ],
        )
        assert result.exit_code != 0

    def test_lip_sync_rejects_text_over_120_characters(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "lip-sync",
                "--mode",
                "text2video",
                "--video-id",
                "video-123",
                "--text",
                "x" * 121,
                "--voice-id",
                "voice-123",
            ],
        )
        assert result.exit_code != 0


# ─── Task Commands ─────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/kling/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/kling/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/kling/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tasks", "t-1", "t-2", "--json"])
        assert result.exit_code == 0


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "kling-v1" in result.output

    def test_aspect_ratios(self, runner):
        result = runner.invoke(cli, ["aspect-ratios"])
        assert result.exit_code == 0
        assert "16:9" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

"""Tests for Gemini CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from gemini_cli.core.output import GEMINI_CHAT_MODELS
from gemini_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "gemini-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "generate" in result.output
        assert "task" in result.output
        assert "wait" in result.output
        assert "video-to-video" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output
        assert "--aspect-ratio" in result.output
        assert "--resolution" in result.output

    def test_help_image_to_video(self, runner):
        result = runner.invoke(cli, ["image-to-video", "--help"])
        assert result.exit_code == 0
        assert "--image-url" in result.output
        assert "--resolution" in result.output

    def test_help_video_to_video(self, runner):
        result = runner.invoke(cli, ["video-to-video", "--help"])
        assert result.exit_code == 0
        assert "--video-url" in result.output
        assert "--resolution" in result.output

    def test_help_generate_content(self, runner):
        result = runner.invoke(cli, ["generate-content", "--help"])
        assert result.exit_code == 0
        assert "--contents" in result.output
        assert "--generation-config" in result.output
        assert "--cached-content" not in result.output

    def test_help_stream_generate_content(self, runner):
        result = runner.invoke(cli, ["stream-generate-content", "--help"])
        assert result.exit_code == 0
        assert "--contents" in result.output
        assert "--cached-content" not in result.output

    def test_chat_model_inventory_matches_api(self):
        assert GEMINI_CHAT_MODELS == [
            "gemini-3.7-flash",
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
            "gemini-3-flash-preview",
            "gemini-3.1-flash-lite",
            "gemini-3.1-pro-preview",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
        ]


class TestChatCommand:
    """Tests for chat commands."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is the capital of France?", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["choices"][0]["message"]["content"] == "The capital of France is Paris."

    @respx.mock
    def test_chat_rich_output(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "Hello"])
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-m", "gemini-2.5-pro", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_new_models(self, runner, mock_chat_response):
        for model in [
            "gemini-2.5-flash-lite",
            "gemini-3.6-flash",
            "gemini-3.7-flash",
            "gemini-3.1-flash-lite",
        ]:
            respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
                return_value=Response(200, json=mock_chat_response)
            )
            result = runner.invoke(
                cli, ["--token", "test-token", "chat", "Hello", "-m", model, "--json"]
            )
            assert result.exit_code == 0, f"Model {model} failed: {result.output}"

    def test_chat_rejects_image_models(self, runner):
        """Image models are native-only; the chat endpoint can't serve them."""
        for model in [
            "gemini-3.1-flash-image",
            "gemini-2.5-flash-image",
            "gemini-3-pro-image",
        ]:
            result = runner.invoke(
                cli, ["--token", "test-token", "chat", "Hello", "-m", model, "--json"]
            )
            assert result.exit_code != 0, f"Model {model} should be rejected"

    def test_generate_content_rejects_chat_only_models(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate-content",
                "--model",
                "gemini-3.6-flash",
                "--contents",
                '[{"parts":[{"text":"Hello"}]}]',
                "--json",
            ],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_chat_with_max_completion_tokens(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--max-completion-tokens", "512", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_service_tier(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "chat", "Hello", "--service-tier", "flex", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_system_prompt(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "chat", "Hello",
                "-s", "You are a helpful assistant", "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_chat_with_temperature(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "--temperature", "0.5", "--json"]
        )
        assert result.exit_code == 0

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0

    @respx.mock
    def test_chat_streams_server_sent_events(self, runner):
        route = respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(
                200,
                content='data: {"choices":[{"delta":{"content":"Hello"}}]}\n\ndata: [DONE]\n\n',
                headers={"content-type": "text/event-stream"},
            )
        )
        result = runner.invoke(cli, ["--token", "test-token", "chat", "Hello", "--stream"])
        assert result.exit_code == 0
        assert 'data: {"choices":[{"delta":{"content":"Hello"}}]}' in result.output
        assert "data: [DONE]" in result.output
        assert json.loads(route.calls.last.request.content)["stream"] is True
        assert route.calls.last.request.headers["accept"] == "text/event-stream"

    @respx.mock
    def test_chat_with_extended_openapi_options(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/gemini/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "--stream",
                "--response-format",
                '{"type":"json_object"}',
                "--tools",
                '[{"type":"function","function":{"name":"lookup"}}]',
                "--tool-choice",
                '{"type":"function","function":{"name":"lookup"}}',
                "--stream-options",
                '{"include_usage":true}',
                "--metadata",
                '{"source":"cli"}',
                "--modalities",
                '["text"]',
                "--web-search-options",
                '{"search_context_size":"medium"}',
                "--store",
                "--logprobs",
                "--top-logprobs",
                "3",
                "--no-parallel-tool-calls",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["stream"] is True
        assert body["response_format"] == {"type": "json_object"}
        assert body["tools"][0]["function"]["name"] == "lookup"
        assert body["tool_choice"]["function"]["name"] == "lookup"
        assert body["stream_options"] == {"include_usage": True}
        assert body["metadata"] == {"source": "cli"}
        assert body["modalities"] == ["text"]
        assert body["web_search_options"] == {"search_context_size": "medium"}
        assert body["store"] is True
        assert body["logprobs"] is True
        assert body["top_logprobs"] == 3
        assert body["parallel_tool_calls"] is False


class TestVideoCommand:
    """Tests for video generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "A sunset over the ocean", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == "task-video-123"

    @respx.mock
    def test_generate_with_aspect_ratio(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "generate", "A sunset",
                "--aspect-ratio", "9:16", "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_image_to_video(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "image-to-video", "Animate this",
                "-i", "https://example.com/photo.jpg", "--json",
            ],
        )
        assert result.exit_code == 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "A sunset"])
        assert result.exit_code != 0

    @respx.mock
    def test_generate_with_resolution(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "generate", "A sunset",
                "--resolution", "1080p", "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_image_to_video_with_resolution(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "image-to-video", "Animate this",
                "-i", "https://example.com/photo.jpg", "--resolution", "1080p", "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_video_to_video(self, runner, mock_video_response):
        route = respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "video-to-video", "Transform this",
                "-v", "https://example.com/video.mp4", "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == "task-video-123"
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["video_urls"] == ["https://example.com/video.mp4"]

    def test_video_to_video_rejects_multiple_urls(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "video-to-video",
                "Transform this",
                "-v",
                "https://example.com/first.mp4",
                "-v",
                "https://example.com/second.mp4",
            ],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_video_to_video_with_resolution(self, runner, mock_video_response):
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=Response(200, json=mock_video_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token", "test-token", "video-to-video", "Transform this",
                "-v", "https://example.com/video.mp4", "--resolution", "1080p", "--json",
            ],
        )
        assert result.exit_code == 0

    def test_video_to_video_no_token(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token", "", "video-to-video", "Transform this",
                "-v", "https://example.com/video.mp4",
            ],
        )
        assert result.exit_code != 0


class TestContentCommands:
    """Tests for native Gemini content commands."""

    @respx.mock
    def test_generate_content_json(self, runner, mock_chat_response):
        route = respx.post(
            "https://api.acedata.cloud/v1beta/models/gemini-2.5-flash:generateContent"
        ).mock(return_value=Response(200, json=mock_chat_response))
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate-content",
                "--model",
                "gemini-2.5-flash",
                "--contents",
                '[{"parts":[{"text":"Hello"}]}]',
                "--generation-config",
                '{"temperature":0.5}',
                "--json",
            ],
        )
        assert result.exit_code == 0
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["contents"] == [{"parts": [{"text": "Hello"}]}]
        assert request_body["generationConfig"] == {"temperature": 0.5}

    @respx.mock
    def test_stream_generate_content_server_sent_events(self, runner):
        route = respx.post(
            "https://api.acedata.cloud/v1beta/models/gemini-3.1-flash-image:streamGenerateContent?alt=sse"
        ).mock(
            return_value=Response(
                200,
                content='data: {"candidates":[{"content":{"parts":[{"text":"Hello"}]}}]}\n\ndata: [DONE]\n\n',
                headers={"content-type": "text/event-stream"},
            )
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "stream-generate-content",
                "--model",
                "gemini-3.1-flash-image",
                "--contents",
                '[{"parts":[{"text":"Hello"}]}]',
                "--alt",
                "sse",
                "--tools",
                '[{"functionDeclarations":[{"name":"lookup"}]}]',
                "--tool-config",
                '{"functionCallingConfig":{"mode":"AUTO"}}',
                "--safety-settings",
                '[{"category":"HARM_CATEGORY_HARASSMENT","threshold":"OFF"}]',
            ],
        )
        assert result.exit_code == 0
        assert 'data: {"candidates":[{"content":{"parts":[{"text":"Hello"}]}}]}' in result.output
        assert "data: [DONE]" in result.output
        request_body = json.loads(route.calls[0].request.content)
        assert request_body["tools"] == [{"functionDeclarations": [{"name": "lookup"}]}]
        assert request_body["toolConfig"] == {"functionCallingConfig": {"mode": "AUTO"}}
        assert request_body["safetySettings"][0]["threshold"] == "OFF"
        assert route.calls[0].request.headers["accept"] == "text/event-stream"


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/gemini/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "task", "task-video-123", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == "task-video-123"
        assert data["trace_id"] == "trace-task-123"

    @respx.mock
    def test_task_rich_output_contains_trace_id(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/gemini/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-video-123"])
        assert result.exit_code == 0
        assert "Trace ID" in result.output
        assert "trace-task-123" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/gemini/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "task-1", "task-2", "--json"]
        )
        assert result.exit_code == 0


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gemini-2.5-flash" in result.output
        assert "gemini-2.5-pro" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

    def test_aspect_ratios(self, runner):
        result = runner.invoke(cli, ["aspect-ratios"])
        assert result.exit_code == 0
        assert "16:9" in result.output
        assert "9:16" in result.output

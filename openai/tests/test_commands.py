"""Tests for CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from openai_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "openai-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "chat" in result.output
        assert "embed" in result.output
        assert "imagine" in result.output

    def test_help_chat(self, runner):
        result = runner.invoke(cli, ["chat", "--help"])
        assert result.exit_code == 0
        assert "MESSAGE" in result.output
        assert "--model" in result.output
        assert "--temperature" in result.output

    def test_help_embed(self, runner):
        result = runner.invoke(cli, ["embed", "--help"])
        assert result.exit_code == 0
        assert "TEXT" in result.output
        assert "--model" in result.output

    def test_help_imagine(self, runner):
        result = runner.invoke(cli, ["imagine", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output

    def test_help_respond(self, runner):
        result = runner.invoke(cli, ["respond", "--help"])
        assert result.exit_code == 0
        assert "MESSAGE" in result.output
        assert "--model" in result.output


# ─── Chat Commands ─────────────────────────────────────────────────────────


class TestChatCommands:
    """Tests for chat commands."""

    @respx.mock
    def test_chat_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is the capital of France?", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "choices" in data

    @respx.mock
    def test_chat_rich_output(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "What is the capital of France?"]
        )
        assert result.exit_code == 0
        assert "Paris" in result.output

    @respx.mock
    def test_chat_with_model(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-m", "gpt-4o", "--json"]
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-4o"

    @respx.mock
    def test_chat_with_system(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "chat",
                "Hello",
                "-s",
                "You are a helpful assistant",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["messages"][0]["role"] == "system"
        assert body["messages"][0]["content"] == "You are a helpful assistant"

    @respx.mock
    def test_chat_with_temperature(self, runner, mock_chat_response):
        route = respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "chat", "Hello", "-t", "0.5", "--json"]
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["temperature"] == 0.5

    def test_chat_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "chat", "Hello"])
        assert result.exit_code != 0


# ─── Complete Commands ─────────────────────────────────────────────────────


class TestCompleteCommands:
    """Tests for the complete command."""

    @respx.mock
    def test_complete_json(self, runner, mock_chat_response):
        respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
            return_value=Response(200, json=mock_chat_response)
        )
        messages = json.dumps([{"role": "user", "content": "Hello"}])
        result = runner.invoke(
            cli, ["--token", "test-token", "complete", messages, "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "choices" in data

    def test_complete_invalid_json(self, runner):
        result = runner.invoke(cli, ["--token", "test-token", "complete", "not-json"])
        assert result.exit_code != 0


# ─── Embed Commands ────────────────────────────────────────────────────────


class TestEmbedCommands:
    """Tests for embed commands."""

    @respx.mock
    def test_embed_json(self, runner, mock_embed_response):
        respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_embed_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "embed", "The quick brown fox", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "data" in data

    @respx.mock
    def test_embed_rich_output(self, runner, mock_embed_response):
        respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_embed_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "embed", "Hello world"]
        )
        assert result.exit_code == 0
        assert "Embeddings" in result.output

    @respx.mock
    def test_embed_with_model(self, runner, mock_embed_response):
        route = respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_embed_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "embed", "Hello", "-m", "text-embedding-3-large", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "text-embedding-3-large"

    @respx.mock
    def test_embed_with_dimensions(self, runner, mock_embed_response):
        route = respx.post("https://api.acedata.cloud/openai/embeddings").mock(
            return_value=Response(200, json=mock_embed_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "embed", "Hello", "--dimensions", "256", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["dimensions"] == 256


# ─── Image Commands ────────────────────────────────────────────────────────


class TestImagineCommands:
    """Tests for image generation commands."""

    @respx.mock
    def test_imagine_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "imagine", "A cat at sunset", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "data" in data

    @respx.mock
    def test_imagine_rich_output(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "imagine", "A cat at sunset"])
        assert result.exit_code == 0
        assert "https://example.com/generated-image.png" in result.output

    @respx.mock
    def test_imagine_with_model(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "A cat", "-m", "gpt-image-1", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "gpt-image-1"

    @respx.mock
    def test_imagine_with_size(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/generations").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "imagine", "A cat", "--size", "1024x1024", "--json"],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["size"] == "1024x1024"


class TestEditImageCommands:
    """Tests for image editing commands."""

    @respx.mock
    def test_edit_image_json(self, runner, mock_image_response):
        respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit-image",
                "Make background white",
                "-i",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "data" in data

    @respx.mock
    def test_edit_image_single_url(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit-image",
                "Remove background",
                "-i",
                "https://example.com/photo.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["image"] == "https://example.com/photo.jpg"

    @respx.mock
    def test_edit_image_multiple_urls(self, runner, mock_image_response):
        route = respx.post("https://api.acedata.cloud/openai/images/edits").mock(
            return_value=Response(200, json=mock_image_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "edit-image",
                "Combine",
                "-i",
                "https://example.com/a.jpg",
                "-i",
                "https://example.com/b.jpg",
                "--json",
            ],
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert isinstance(body["image"], list)
        assert len(body["image"]) == 2


# ─── Respond Commands ──────────────────────────────────────────────────────


class TestRespondCommands:
    """Tests for respond commands."""

    @respx.mock
    def test_respond_json(self, runner, mock_responses_response):
        respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_responses_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "respond", "What is 2+2?", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "choices" in data

    @respx.mock
    def test_respond_with_model(self, runner, mock_responses_response):
        route = respx.post("https://api.acedata.cloud/openai/responses").mock(
            return_value=Response(200, json=mock_responses_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "respond", "Hello", "-m", "o3", "--json"]
        )
        assert result.exit_code == 0
        body = json.loads(route.calls.last.request.content)
        assert body["model"] == "o3"


# ─── Info Commands ─────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "gpt-4o" in result.output
        assert "gpt-5.4" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

"""Tests for Fish CLI commands."""

import json

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from fish_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "fish-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "tts" in result.output
        assert "models" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_tts(self, runner):
        result = runner.invoke(cli, ["tts", "--help"])
        assert result.exit_code == 0
        assert "TEXT" in result.output
        assert "--model" in result.output
        assert "--reference-id" in result.output
        assert "--format" in result.output
        assert "--opus-bitrate" in result.output
        assert "--prosody" in result.output
        assert "--references" in result.output

    def test_help_models(self, runner):
        result = runner.invoke(cli, ["models", "--help"])
        assert result.exit_code == 0
        assert "--page-size" in result.output
        assert "--title-language" in result.output
        assert "--sort-by" in result.output

    def test_help_model(self, runner):
        result = runner.invoke(cli, ["model", "--help"])
        assert result.exit_code == 0
        assert "MODEL_ID" in result.output


class TestTTSCommand:
    """Tests for TTS generation commands."""

    @respx.mock
    def test_tts_json(self, runner, mock_tts_response):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tts", "Hello, world!", "--json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "audio_url" in data
        assert "fish.audio" in data["audio_url"]

    @respx.mock
    def test_tts_rich_output(self, runner, mock_tts_response):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "tts", "Hello"])
        assert result.exit_code == 0
        assert "fish.audio" in result.output

    @respx.mock
    def test_tts_with_reference_id(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tts",
                "Hello",
                "--reference-id",
                "d7900c21663f485ab63ebdb7e5905036",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["reference_id"] == "d7900c21663f485ab63ebdb7e5905036"

    @respx.mock
    def test_tts_with_format(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tts", "Hello", "--format", "wav", "--json"]
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["format"] == "wav"

    @respx.mock
    def test_tts_with_latency(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tts", "Hello", "--latency", "balanced", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["latency"] == "balanced"

    @respx.mock
    def test_tts_with_temperature(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tts", "Hello", "--temperature", "0.8", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["temperature"] == 0.8

    @respx.mock
    def test_tts_with_callback_url(self, runner, mock_tts_async_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_async_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tts",
                "Hello",
                "--callback-url",
                "https://webhook.site/test",
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["callback_url"] == "https://webhook.site/test"

    @respx.mock
    def test_tts_with_additional_openapi_fields(self, runner, mock_tts_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "tts",
                "Hello",
                "--opus-bitrate",
                "64000",
                "--chunk-length",
                "120",
                "--min-chunk-length",
                "30",
                "--prosody",
                '{"speed": 1.1}',
                "--references",
                '[{"audio":"https://example.com/ref.wav"}]',
                "--json",
            ],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["opus_bitrate"] == 64000
        assert sent["chunk_length"] == 120
        assert sent["min_chunk_length"] == 30
        assert sent["prosody"] == {"speed": 1.1}
        assert sent["references"] == [{"audio": "https://example.com/ref.wav"}]

    def test_tts_with_invalid_prosody_json(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tts", "Hello", "--prosody", "not-json"],
        )
        assert result.exit_code != 0
        assert "--prosody must be valid JSON." in result.output

    def test_tts_with_invalid_references_json(self, runner):
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tts", "Hello", "--references", '{"a":1}'],
        )
        assert result.exit_code != 0
        assert "--references must be a JSON array." in result.output

    @respx.mock
    def test_tts_async(self, runner, mock_tts_async_response):
        route = respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_async_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tts", "Hello", "--async", "--json"]
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["async"] is True

    @respx.mock
    def test_tts_async_rich_output(self, runner, mock_tts_async_response):
        respx.post("https://api.acedata.cloud/fish/tts").mock(
            return_value=Response(200, json=mock_tts_async_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tts", "Hello", "--async"]
        )
        assert result.exit_code == 0
        assert "2725a2d3" in result.output

    def test_tts_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "tts", "Hello"])
        assert result.exit_code != 0


class TestModelCommands:
    """Tests for model query commands."""

    @respx.mock
    def test_models_json(self, runner, mock_models_response):
        respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json=mock_models_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "models", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "items" in data
        assert data["total"] == 1

    @respx.mock
    def test_models_rich_output(self, runner, mock_models_response):
        respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json=mock_models_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "models"])
        assert result.exit_code == 0
        assert "My Cloned Voice" in result.output

    @respx.mock
    def test_models_with_self_flag(self, runner, mock_models_response):
        route = respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json=mock_models_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "models", "--self", "--json"])
        assert result.exit_code == 0
        assert "self=true" in str(route.calls[0].request.url)

    @respx.mock
    def test_models_with_new_query_params(self, runner, mock_models_response):
        route = respx.get("https://api.acedata.cloud/fish/model").mock(
            return_value=Response(200, json=mock_models_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "models",
                "--title-language",
                "en",
                "--sort-by",
                "created_at",
                "--json",
            ],
        )
        assert result.exit_code == 0
        assert "title_language=en" in str(route.calls[0].request.url)
        assert "sort_by=created_at" in str(route.calls[0].request.url)

    @respx.mock
    def test_model_get_json(self, runner, mock_model_response):
        respx.get("https://api.acedata.cloud/fish/model/d7900c21663f485ab63ebdb7e5905036").mock(
            return_value=Response(200, json=mock_model_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "model",
                "d7900c21663f485ab63ebdb7e5905036",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["_id"] == "d7900c21663f485ab63ebdb7e5905036"
        assert data["title"] == "My Cloned Voice"

    @respx.mock
    def test_model_get_rich_output(self, runner, mock_model_response):
        respx.get("https://api.acedata.cloud/fish/model/d7900c21663f485ab63ebdb7e5905036").mock(
            return_value=Response(200, json=mock_model_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "model", "d7900c21663f485ab63ebdb7e5905036"]
        )
        assert result.exit_code == 0
        assert "My Cloned Voice" in result.output


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "task",
                "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["id"] == "2725a2d3-f87e-4905-9c53-9988d5a7b2f5"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "2725a2d3-f87e-4905-9c53-9988d5a7b2f5"],
        )
        assert result.exit_code == 0
        assert "2725a2d3" in result.output

    @respx.mock
    def test_tasks_batch_json(self, runner, mock_tasks_batch_response):
        respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_tasks_batch_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "tasks", "abc123", "def456", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["count"] == 2

    @respx.mock
    def test_task_sends_correct_payload(self, runner, mock_task_response):
        route = respx.post("https://api.acedata.cloud/fish/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "task", "my-task-id", "--json"],
        )
        assert result.exit_code == 0
        sent = json.loads(route.calls[0].request.content)
        assert sent["id"] == "my-task-id"
        assert sent["action"] == "retrieve"


class TestInfoCommands:
    """Tests for info and utility commands."""

    def test_tts_models(self, runner):
        result = runner.invoke(cli, ["tts-models"])
        assert result.exit_code == 0
        assert "s2-pro" in result.output
        assert "s2.1-pro" in result.output
        assert "s1" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "api.acedata.cloud" in result.output

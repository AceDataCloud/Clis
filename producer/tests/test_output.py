"""Tests for output formatting."""

from producer_cli.core.output import (
    AUDIO_ACTIONS,
    DEFAULT_MODEL,
    PRODUCER_MODELS,
    print_audio_result,
    print_error,
    print_json,
    print_lyrics_result,
    print_models,
    print_success,
    print_task_result,
    print_upload_result,
)


class TestConstants:
    """Tests for output constants."""

    def test_models_count(self):
        assert len(PRODUCER_MODELS) == 8

    def test_default_model_in_models(self):
        assert DEFAULT_MODEL in PRODUCER_MODELS

    def test_models_include_all(self):
        for model in [
            "FUZZ-2.0 Pro",
            "FUZZ-2.0",
            "FUZZ-2.0 Raw",
            "FUZZ-1.1 Pro",
            "FUZZ-1.0 Pro",
            "FUZZ-1.0",
            "FUZZ-1.1",
            "FUZZ-0.8",
        ]:
            assert model in PRODUCER_MODELS

    def test_actions_count(self):
        assert len(AUDIO_ACTIONS) == 8

    def test_actions_include_all(self):
        for action in [
            "generate",
            "cover",
            "extend",
            "variation",
            "swap_vocals",
            "swap_instrumentals",
            "replace_section",
            "stems",
        ]:
            assert action in AUDIO_ACTIONS


class TestPrintJson:
    """Tests for JSON output."""

    def test_print_json_dict(self, capsys):
        print_json({"key": "value"})
        captured = capsys.readouterr()
        assert '"key": "value"' in captured.out

    def test_print_json_unicode(self, capsys):
        print_json({"text": "你好世界"})
        captured = capsys.readouterr()
        assert "你好世界" in captured.out

    def test_print_json_nested(self, capsys):
        print_json({"data": [{"id": "123"}]})
        captured = capsys.readouterr()
        assert '"id": "123"' in captured.out


class TestPrintMessages:
    """Tests for message output."""

    def test_print_error(self, capsys):
        print_error("Something went wrong")
        captured = capsys.readouterr()
        assert "Something went wrong" in captured.out

    def test_print_success(self, capsys):
        print_success("Done!")
        captured = capsys.readouterr()
        assert "Done!" in captured.out


class TestPrintAudioResult:
    """Tests for audio result formatting."""

    def test_print_audio_result(self, capsys):
        data = {
            "task_id": "task-123",
            "trace_id": "trace-456",
            "data": [
                {
                    "audio_url": "https://cdn.example.com/audio.mp3",
                    "state": "succeeded",
                    "title": "Test Song",
                    "model_name": "FUZZ-2.0",
                }
            ],
        }
        print_audio_result(data)
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_audio_result_empty_data(self, capsys):
        data = {"task_id": "t-123", "trace_id": "tr-456", "data": []}
        print_audio_result(data)
        captured = capsys.readouterr()
        assert "t-123" in captured.out


class TestPrintLyricsResult:
    """Tests for lyrics result formatting."""

    def test_print_lyrics_result(self, capsys):
        data = {
            "data": {
                "text": "[Verse]\nTest lyrics",
                "title": "My Song",
                "status": "complete",
            }
        }
        print_lyrics_result(data)
        captured = capsys.readouterr()
        assert "Test lyrics" in captured.out

    def test_print_lyrics_result_empty(self, capsys):
        data = {"data": {}}
        print_lyrics_result(data)
        captured = capsys.readouterr()
        assert captured.out  # Should produce some output


class TestPrintUploadResult:
    """Tests for upload result formatting."""

    def test_print_upload_result(self, capsys):
        data = {
            "success": True,
            "data": {
                "audio_id": "uploaded-123",
                "audio_url": "https://cdn.example.com/uploaded.mp3",
            },
        }
        print_upload_result(data)
        captured = capsys.readouterr()
        assert "uploaded-123" in captured.out


class TestPrintTaskResult:
    """Tests for task result formatting."""

    def test_print_task_result(self, capsys):
        data = {
            "data": [
                {
                    "id": "task-123",
                    "status": "completed",
                    "audio_url": "https://cdn.example.com/result.mp3",
                }
            ]
        }
        print_task_result(data)
        captured = capsys.readouterr()
        assert "task-123" in captured.out


class TestPrintModels:
    """Tests for models display."""

    def test_print_models(self, capsys):
        print_models()
        captured = capsys.readouterr()
        assert "FUZZ-2.0" in captured.out

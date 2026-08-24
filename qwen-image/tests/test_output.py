"""Tests for output formatting."""

from qwen_image_cli.core.output import (
    DEFAULT_MODEL,
    PROMPT_EXTEND_MODES,
    QWEN_IMAGE_MODELS,
    print_error,
    print_image_result,
    print_json,
    print_models,
    print_success,
    print_task_result,
)


class TestConstants:
    """Tests for output constants."""

    def test_models_count(self):
        assert len(QWEN_IMAGE_MODELS) == 2

    def test_default_model_in_models(self):
        assert DEFAULT_MODEL in QWEN_IMAGE_MODELS

    def test_models_include_all(self):
        assert "qwen-image-3.0" in QWEN_IMAGE_MODELS
        assert "qwen-image-3.0-pro" in QWEN_IMAGE_MODELS

    def test_prompt_extend_modes(self):
        assert PROMPT_EXTEND_MODES == ["direct", "agent"]


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


class TestPrintImageResult:
    """Tests for image result formatting."""

    def test_print_image_result(self, capsys):
        data = {
            "task_id": "img-task-123",
            "trace_id": "trace-456",
            "data": [
                {
                    "image_url": "https://cdn.example.com/image.png",
                    "state": "succeeded",
                    "model_name": "qwen-image-3.0",
                }
            ],
        }
        print_image_result(data)
        captured = capsys.readouterr()
        assert "img-task-123" in captured.out

    def test_print_image_result_empty_data(self, capsys):
        data = {"task_id": "t-123", "trace_id": "tr-456", "data": []}
        print_image_result(data)
        captured = capsys.readouterr()
        assert "t-123" in captured.out


class TestPrintTaskResult:
    """Tests for task result formatting."""

    def test_print_task_result(self, capsys):
        data = {
            "data": [
                {
                    "id": "task-123",
                    "status": "completed",
                    "image_url": "https://cdn.example.com/result.png",
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
        assert "qwen-image-3.0" in captured.out
        assert "qwen-image-3.0-pro" in captured.out

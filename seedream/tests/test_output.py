"""Tests for output formatting."""

from seedream_cli.core.output import (
    DEFAULT_MODEL,
    RESOLUTIONS,
    SEEDREAM_MODELS,
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
        assert len(SEEDREAM_MODELS) == 5

    def test_default_model_in_models(self):
        assert DEFAULT_MODEL in SEEDREAM_MODELS

    def test_models_include_all(self):
        for model in [
            "doubao-seedream-5-0-260128",
            "doubao-seedream-4-5-251128",
            "doubao-seedream-4-0-250828",
            "doubao-seedream-3-0-t2i-250415",
            "doubao-seededit-3-0-i2i-250628",
        ]:
            assert model in SEEDREAM_MODELS

    def test_resolutions(self):
        assert len(RESOLUTIONS) == 5


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
            "task_id": "task-123",
            "trace_id": "trace-456",
            "data": [
                {
                    "image_url": "https://cdn.example.com/image.png",
                    "state": "succeeded",
                    "model_name": "doubao-seedream-4-0-250828",
                }
            ],
        }
        print_image_result(data)
        captured = capsys.readouterr()
        assert "task-123" in captured.out

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
        assert "doubao-seedream-4-5-251128" in captured.out

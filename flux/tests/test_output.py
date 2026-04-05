"""Tests for output formatting."""

from flux_cli.core.output import (
    ASPECT_RATIOS,
    FLUX_MODELS,
    print_error,
    print_image_result,
    print_json,
    print_success,
    print_task_result,
)


class TestConstants:
    """Tests for output constants."""

    def test_flux_models(self):
        assert len(FLUX_MODELS) == 6
        assert "flux-dev" in FLUX_MODELS
        assert "flux-kontext-pro" in FLUX_MODELS

    def test_aspect_ratios(self):
        assert len(ASPECT_RATIOS) == 11
        assert "16:9" in ASPECT_RATIOS
        assert "1:1" in ASPECT_RATIOS


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
                    "model": "flux-dev",
                    "created_at": "2025-01-21T00:00:00.000Z",
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

    def test_print_image_result_no_data(self, capsys):
        data = {"task_id": "t-123", "trace_id": "tr-456"}
        print_image_result(data)
        captured = capsys.readouterr()
        assert "t-123" in captured.out


class TestPrintTaskResult:
    """Tests for task result formatting."""

    def test_print_task_result_data_array(self, capsys):
        data = {
            "data": [
                {
                    "image_url": "https://cdn.example.com/result.png",
                    "model": "flux-dev",
                    "created_at": "2025-01-21T00:00:00.000Z",
                }
            ]
        }
        print_task_result(data)
        captured = capsys.readouterr()
        assert "cdn.example.com" in captured.out

    def test_print_task_result_batch(self, capsys):
        data = {
            "items": [
                {
                    "id": "task-1",
                    "type": "image",
                    "created_at": "2025-01-21T00:00:00.000Z",
                    "response": {"data": [{"image_url": "https://cdn.example.com/img1.png"}]},
                }
            ]
        }
        print_task_result(data)
        captured = capsys.readouterr()
        assert "task-1" in captured.out

    def test_print_task_result_empty(self, capsys):
        data = {"data": [], "items": []}
        print_task_result(data)
        captured = capsys.readouterr()
        assert "No data" in captured.out

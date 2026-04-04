"""Tests for output formatting."""

from seedance_cli.core.output import (
    ASPECT_RATIOS,
    DEFAULT_MODEL,
    RESOLUTIONS,
    SEEDANCE_MODELS,
    print_error,
    print_json,
    print_models,
    print_success,
    print_task_result,
    print_video_result,
)


class TestConstants:
    """Tests for output constants."""

    def test_models_count(self):
        assert len(SEEDANCE_MODELS) == 5

    def test_default_model_in_models(self):
        assert DEFAULT_MODEL in SEEDANCE_MODELS

    def test_models_include_all(self):
        for model in [
            "doubao-seedance-1-5-pro-251215",
            "doubao-seedance-1-0-pro-250528",
            "doubao-seedance-1-0-pro-fast-251015",
            "doubao-seedance-1-0-lite-t2v-250428",
            "doubao-seedance-1-0-lite-i2v-250428",
        ]:
            assert model in SEEDANCE_MODELS

    def test_aspect_ratios(self):
        assert len(ASPECT_RATIOS) == 7
        assert "16:9" in ASPECT_RATIOS
        assert "adaptive" in ASPECT_RATIOS

    def test_resolutions(self):
        assert len(RESOLUTIONS) == 3


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


class TestPrintVideoResult:
    """Tests for video result formatting."""

    def test_print_video_result(self, capsys):
        data = {
            "task_id": "task-123",
            "trace_id": "trace-456",
            "data": [
                {
                    "video_url": "https://cdn.example.com/video.mp4",
                    "state": "succeeded",
                    "model_name": "doubao-seedance-1-0-pro-250528",
                }
            ],
        }
        print_video_result(data)
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_video_result_empty_data(self, capsys):
        data = {"task_id": "t-123", "trace_id": "tr-456", "data": []}
        print_video_result(data)
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
                    "video_url": "https://cdn.example.com/result.mp4",
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
        assert "seedance-1-5-pro" in captured.out

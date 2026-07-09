"""Tests for HappyHorse CLI output formatting."""

from happyhorse_cli.core.output import (
    HAPPYHORSE_MODELS,
    print_error,
    print_json,
    print_models,
    print_success,
    print_task_result,
    print_video_result,
)


class TestOutputFunctions:
    """Tests for output formatting functions."""

    def test_print_json(self, capsys):
        print_json({"key": "value"})
        captured = capsys.readouterr()
        assert '"key": "value"' in captured.out

    def test_print_error(self, capsys):
        print_error("Something went wrong")
        captured = capsys.readouterr()
        assert "Something went wrong" in captured.out

    def test_print_success(self, capsys):
        print_success("Done!")
        captured = capsys.readouterr()
        assert "Done!" in captured.out

    def test_print_video_result_with_url(self, capsys):
        print_video_result(
            {
                "task_id": "task-123",
                "trace_id": "trace-456",
                "data": [
                    {
                        "id": "item-1",
                        "video_url": "https://cdn.example.com/video.mp4",
                        "state": "succeeded",
                    }
                ],
            }
        )
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_video_result_pending(self, capsys):
        print_video_result({"task_id": "task-123", "trace_id": "trace-456"})
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_task_result_single(self, capsys):
        print_task_result(
            {
                "success": True,
                "data": {
                    "id": "task-123",
                    "state": "succeeded",
                    "video_url": "https://cdn.example.com/video.mp4",
                },
            }
        )
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_task_result_batch(self, capsys):
        print_task_result(
            {
                "success": True,
                "data": [
                    {"id": "task-1", "state": "succeeded"},
                    {"id": "task-2", "state": "succeeded"},
                ],
            }
        )
        captured = capsys.readouterr()
        assert "task-1" in captured.out

    def test_print_models(self, capsys):
        print_models()
        captured = capsys.readouterr()
        assert "happyhorse-1.1-t2v" in captured.out

    def test_happyhorse_models_list(self):
        assert "happyhorse-1.0-t2v" in HAPPYHORSE_MODELS
        assert "happyhorse-1.1-t2v" in HAPPYHORSE_MODELS
        assert "happyhorse-1.0-i2v" in HAPPYHORSE_MODELS
        assert "happyhorse-1.1-i2v" in HAPPYHORSE_MODELS
        assert "happyhorse-1.0-r2v" in HAPPYHORSE_MODELS
        assert "happyhorse-1.1-r2v" in HAPPYHORSE_MODELS
        assert "happyhorse-1.0-video-edit" in HAPPYHORSE_MODELS

"""Tests for MiniMax CLI output formatting."""

from minimax_cli.core.output import (
    MINIMAX_MODELS,
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
                "video_url": "https://cdn.example.com/video.mp4",
            }
        )
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_video_result_pending(self, capsys):
        print_video_result({"task_id": "task-123", "trace_id": "trace-456"})
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_video_result_synchronous(self, capsys):
        print_video_result(
            {
                "task": {
                    "id": "task-123",
                    "content": {"url": "https://cdn.example.com/video.mp4"},
                }
            }
        )
        captured = capsys.readouterr()
        assert "task-123" in captured.out
        assert "https://cdn.example.com/video.mp4" in captured.out

    def test_print_task_result_single(self, capsys):
        print_task_result(
            {
                "task": {
                    "id": "task-123",
                    "status": "succeeded",
                    "content": {"url": "https://cdn.example.com/video.mp4"},
                },
            }
        )
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_task_result_batch(self, capsys):
        print_task_result(
            {
                "items": [
                    {"id": "task-1", "status": "succeeded"},
                    {"id": "task-2", "status": "succeeded"},
                ],
                "total": 2,
            }
        )
        captured = capsys.readouterr()
        assert "task-1" in captured.out

    def test_print_models(self, capsys):
        print_models()
        captured = capsys.readouterr()
        for model in MINIMAX_MODELS:
            assert model in captured.out

    def test_minimax_models_list(self):
        assert MINIMAX_MODELS == ["MiniMax-H3"]

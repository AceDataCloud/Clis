"""Tests for output formatting."""

from midjourney_cli.core.output import (
    IMAGINE_ACTIONS,
    MIDJOURNEY_MODES,
    MIDJOURNEY_VERSIONS,
    VIDEO_MODES,
    VIDEO_RESOLUTIONS,
    print_describe_result,
    print_error,
    print_imagine_result,
    print_json,
    print_seed_result,
    print_success,
    print_task_result,
    print_translate_result,
    print_video_result,
)


class TestConstants:
    """Tests for output constants."""

    def test_modes(self):
        assert len(MIDJOURNEY_MODES) == 3
        assert "fast" in MIDJOURNEY_MODES

    def test_versions(self):
        assert "8" in MIDJOURNEY_VERSIONS

    def test_actions(self):
        assert "generate" in IMAGINE_ACTIONS
        assert "upscale1" in IMAGINE_ACTIONS

    def test_video_modes(self):
        assert len(VIDEO_MODES) == 2
        assert "relax" not in VIDEO_MODES

    def test_video_resolutions(self):
        assert "720p" in VIDEO_RESOLUTIONS


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


class TestPrintImagineResult:
    """Tests for imagine result formatting."""

    def test_print_imagine_result(self, capsys):
        data = {
            "task_id": "task-123",
            "trace_id": "trace-456",
            "image_url": "https://cdn.example.com/image.png",
            "image_id": "img-789",
            "image_width": 1024,
            "image_height": 1024,
            "actions": ["upscale1", "upscale2"],
        }
        print_imagine_result(data)
        captured = capsys.readouterr()
        assert "task-123" in captured.out

    def test_print_imagine_result_no_image(self, capsys):
        data = {"task_id": "t-123", "trace_id": "tr-456"}
        print_imagine_result(data)
        captured = capsys.readouterr()
        assert "t-123" in captured.out


class TestPrintDescribeResult:
    """Tests for describe result formatting."""

    def test_print_describe_result(self, capsys):
        data = {"descriptions": ["A sunset", "Mountains"]}
        print_describe_result(data)
        captured = capsys.readouterr()
        assert "sunset" in captured.out

    def test_print_describe_result_empty(self, capsys):
        data = {"descriptions": []}
        print_describe_result(data)
        captured = capsys.readouterr()
        assert "No descriptions" in captured.out


class TestPrintVideoResult:
    """Tests for video result formatting."""

    def test_print_video_result(self, capsys):
        data = {
            "task_id": "vid-123",
            "trace_id": "tr-456",
            "video_urls": ["https://example.com/v1.mp4"],
        }
        print_video_result(data)
        captured = capsys.readouterr()
        assert "vid-123" in captured.out


class TestPrintTranslateResult:
    """Tests for translate result formatting."""

    def test_print_translate_result(self, capsys):
        data = {"translated_content": "A cat on a table"}
        print_translate_result(data)
        captured = capsys.readouterr()
        assert "cat" in captured.out


class TestPrintSeedResult:
    """Tests for seed result formatting."""

    def test_print_seed_result(self, capsys):
        data = {"seed": 12345}
        print_seed_result(data)
        captured = capsys.readouterr()
        assert "12345" in captured.out


class TestPrintTaskResult:
    """Tests for task result formatting."""

    def test_print_task_result_image(self, capsys):
        data = {
            "image_url": "https://cdn.example.com/result.png",
            "image_id": "img-123",
        }
        print_task_result(data)
        captured = capsys.readouterr()
        assert "result.png" in captured.out

"""Tests for output formatting."""

import json

from adc_cli.core.output import (
    SERVICES,
    print_error,
    print_json,
    print_result,
    print_search_result,
    print_services,
    print_success,
    print_task_result,
)


class TestConstants:
    """Tests for output constants."""

    def test_services_catalog(self):
        assert len(SERVICES) == 10
        assert "flux" in SERVICES
        assert "midjourney" in SERVICES
        assert "suno" in SERVICES
        assert "luma" in SERVICES
        assert "sora" in SERVICES
        assert "serp" in SERVICES

    def test_service_structure(self):
        for name, info in SERVICES.items():
            assert "type" in info, f"{name} missing type"
            assert "description" in info, f"{name} missing description"
            assert info["type"] in ("Image", "Video", "Music", "Search")


class TestPrintJson:
    """Tests for JSON output."""

    def test_print_json(self, capsys):
        data = {"key": "value", "number": 42}
        print_json(data)
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["key"] == "value"
        assert parsed["number"] == 42

    def test_print_json_unicode(self, capsys):
        data = {"text": "中文测试"}
        print_json(data)
        captured = capsys.readouterr()
        assert "中文测试" in captured.out


class TestPrintFunctions:
    """Tests for Rich print functions."""

    def test_print_error(self, capsys):
        print_error("something went wrong")
        captured = capsys.readouterr()
        assert "something went wrong" in captured.out

    def test_print_success(self, capsys):
        print_success("done!")
        captured = capsys.readouterr()
        assert "done!" in captured.out

    def test_print_result_with_data(self, capsys, mock_image_response):
        print_result(mock_image_response, "Image Result")
        captured = capsys.readouterr()
        assert "test-task-123" in captured.out
        assert "Image Result" in captured.out

    def test_print_result_no_data(self, capsys):
        print_result({"task_id": "abc", "trace_id": "def", "data": []}, "Result")
        captured = capsys.readouterr()
        assert "No data available" in captured.out

    def test_print_task_result_with_data(self, capsys, mock_task_response):
        print_task_result(mock_task_response)
        captured = capsys.readouterr()
        assert "result.png" in captured.out

    def test_print_task_result_no_data(self, capsys):
        print_task_result({"data": []})
        captured = capsys.readouterr()
        assert "No data available" in captured.out

    def test_print_search_result_organic(self, capsys, mock_search_response):
        print_search_result(mock_search_response)
        captured = capsys.readouterr()
        assert "Artificial Intelligence" in captured.out

    def test_print_search_result_empty(self, capsys):
        print_search_result({})
        captured = capsys.readouterr()
        assert "No results found" in captured.out

    def test_print_services(self, capsys):
        print_services()
        captured = capsys.readouterr()
        assert "flux" in captured.out
        assert "suno" in captured.out
        assert "luma" in captured.out

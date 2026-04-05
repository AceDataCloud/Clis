"""Tests for output formatting."""

from serp_cli.core.output import (
    SEARCH_TYPES,
    print_error,
    print_json,
    print_search_result,
    print_search_types,
    print_success,
)


class TestConstants:
    """Tests for output constants."""

    def test_search_types(self):
        assert len(SEARCH_TYPES) == 6
        assert "search" in SEARCH_TYPES
        assert "images" in SEARCH_TYPES
        assert "news" in SEARCH_TYPES


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


class TestPrintSearchResult:
    """Tests for search result formatting."""

    def test_print_organic_results(self, capsys):
        data = {
            "organic": [
                {
                    "title": "Test Result",
                    "link": "https://example.com",
                    "snippet": "A test search result.",
                }
            ],
        }
        print_search_result(data)
        captured = capsys.readouterr()
        assert "Test Result" in captured.out

    def test_print_knowledge_graph(self, capsys):
        data = {
            "knowledge_graph": {
                "title": "Test Entity",
                "description": "A test description.",
            },
        }
        print_search_result(data)
        captured = capsys.readouterr()
        assert "Test Entity" in captured.out

    def test_print_news_results(self, capsys):
        data = {
            "news": [
                {
                    "title": "Breaking News",
                    "source": "TestSource",
                    "date": "1 hour ago",
                }
            ],
        }
        print_search_result(data)
        captured = capsys.readouterr()
        assert "Breaking News" in captured.out

    def test_print_empty_results(self, capsys):
        data = {}
        print_search_result(data)
        captured = capsys.readouterr()
        assert "No results found" in captured.out

    def test_print_people_also_ask(self, capsys):
        data = {
            "people_also_ask": [
                {"question": "What is AI?"},
            ],
        }
        print_search_result(data)
        captured = capsys.readouterr()
        assert "What is AI?" in captured.out

    def test_print_related_searches(self, capsys):
        data = {
            "related_searches": [
                {"query": "machine learning"},
            ],
        }
        print_search_result(data)
        captured = capsys.readouterr()
        assert "machine learning" in captured.out


class TestPrintSearchTypes:
    """Tests for search types display."""

    def test_print_search_types(self, capsys):
        print_search_types()
        captured = capsys.readouterr()
        assert "search" in captured.out
        assert "images" in captured.out

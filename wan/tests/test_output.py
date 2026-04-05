"""Tests for output formatting."""

import json

from wan_cli.core.output import (
    DEFAULT_MODEL,
    DURATIONS,
    RESOLUTIONS,
    SHOT_TYPES,
    WAN_MODELS,
    print_error,
    print_json,
    print_models,
    print_success,
    print_task_result,
    print_video_result,
)


def test_wan_models_list():
    assert "wan2.6-t2v" in WAN_MODELS
    assert "wan2.6-i2v" in WAN_MODELS
    assert "wan2.6-i2v-flash" in WAN_MODELS
    assert "wan2.6-r2v" in WAN_MODELS


def test_default_model():
    assert DEFAULT_MODEL == "wan2.6-t2v"


def test_resolutions():
    assert "480P" in RESOLUTIONS
    assert "720P" in RESOLUTIONS
    assert "1080P" in RESOLUTIONS


def test_shot_types():
    assert "single" in SHOT_TYPES
    assert "multi" in SHOT_TYPES


def test_durations():
    assert 5 in DURATIONS
    assert 10 in DURATIONS
    assert 15 in DURATIONS


def test_print_json(capsys):
    data = {"key": "value", "number": 42}
    print_json(data)
    # Output goes to console, not capsys - just verify no exception


def test_print_error_no_exception():
    print_error("Test error message")


def test_print_success_no_exception():
    print_success("Test success message")


def test_print_models_no_exception():
    print_models()


def test_print_video_result_no_exception():
    data = {
        "task_id": "test-123",
        "trace_id": "trace-456",
        "data": [
            {
                "id": "video-1",
                "state": "succeeded",
                "video_url": "https://example.com/video.mp4",
            }
        ],
    }
    print_video_result(data)


def test_print_video_result_empty():
    print_video_result({"task_id": "t-1", "data": []})


def test_print_task_result_list():
    data = {
        "data": [
            {
                "id": "task-1",
                "state": "succeeded",
                "video_url": "https://example.com/video.mp4",
            }
        ]
    }
    print_task_result(data)


def test_print_task_result_dict():
    data = {
        "data": {
            "id": "task-1",
            "state": "succeeded",
        }
    }
    print_task_result(data)

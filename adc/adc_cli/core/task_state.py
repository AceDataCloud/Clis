"""Terminal-state helpers for media task records."""

from typing import Any


def acemusic_task_state(result: dict[str, Any]) -> str:
    state = str(result.get("state") or result.get("status") or "").lower()
    terminal = {
        "succeeded",
        "complete",
        "completed",
        "partial_failed",
        "failed",
        "error",
        "cancelled",
        "canceled",
    }
    if state in terminal:
        return state
    response = result.get("response") or {}
    if isinstance(response, dict):
        status = str(response.get("state") or response.get("status") or "").lower()
        if status in terminal:
            return status
        if response.get("success") is False:
            return "failed"
        if response.get("success") is True and response.get("data"):
            return "succeeded"
    return state or "pending"


def media_task_state(record: dict[str, Any]) -> str:
    """Inspect an OpenAI image or Kling task record's nested API response."""
    body = record.get("response") or {}
    if not isinstance(body, dict):
        return "finished_without_media" if record.get("finished_at") else "pending"
    state = str(body.get("state") or body.get("status") or "").lower()
    if (
        body.get("success") is False
        or body.get("error")
        or state in {"failed", "error", "cancelled", "canceled"}
    ):
        return "failed"
    images = body.get("data")
    if body.get("video_url") or (
        isinstance(images, list)
        and any(
            isinstance(item, dict) and (item.get("url") or item.get("b64_json")) for item in images
        )
    ):
        return "completed"
    if record.get("finished_at") or state in {"succeeded", "completed", "complete"}:
        return "finished_without_media"
    return "pending"

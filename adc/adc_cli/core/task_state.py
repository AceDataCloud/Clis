"""ACE Music group completion, separate from individual candidate URLs."""

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

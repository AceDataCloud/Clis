"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file for tests
load_dotenv(dotenv_path=project_root / ".env")

# Set default log level for tests
os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture
def api_token():
    """Get API token from environment for integration tests."""
    token = os.environ.get("ACEDATACLOUD_API_TOKEN", "")
    if not token:
        pytest.skip("ACEDATACLOUD_API_TOKEN not configured for integration tests")
    return token


@pytest.fixture
def mock_audio_response():
    """Mock successful audio generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "id": "audio-id-1",
                "title": "Test Song",
                "style": "pop, upbeat",
                "duration": 120.5,
                "state": "succeeded",
                "model_name": "chirp-v4-5",
                "audio_url": "https://cdn1.suno.ai/test-audio.mp3",
                "video_url": "https://cdn1.suno.ai/test-video.mp4",
                "image_url": "https://cdn2.suno.ai/test-image.jpeg",
                "lyric": "[Verse]\nTest lyrics here\n[Chorus]\nTest chorus here",
                "created_at": "2025-01-21T00:00:00.000Z",
            }
        ],
    }


@pytest.fixture
def mock_lyrics_response():
    """Mock successful lyrics generation response."""
    return {
        "success": True,
        "task_id": "lyrics-task-123",
        "data": [
            {
                "title": "Test Song Title",
                "text": "[Verse]\nGenerated lyrics here\n[Chorus]\nCatchy chorus",
                "status": "complete",
            }
        ],
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "success": True,
        "data": [
            {
                "id": "task-123",
                "status": "completed",
                "audio_url": "https://cdn1.suno.ai/test.mp3",
                "title": "Test Song",
                "duration": 120.5,
            }
        ],
    }


@pytest.fixture
def mock_persona_response():
    """Mock persona creation response."""
    return {
        "success": True,
        "task_id": "persona-task-123",
        "data": {
            "id": "persona-id-456",
            "name": "My Voice",
        },
    }


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {
        "success": False,
        "error": {
            "code": "invalid_request",
            "message": "Invalid parameters provided",
        },
    }


@pytest.fixture
def mock_media_response():
    """Mock media conversion response (MP4/timing)."""
    return {
        "success": True,
        "data": {
            "video_url": "https://cdn1.suno.ai/test-video.mp4",
        },
    }


@pytest.fixture
def mock_wav_response():
    """Mock WAV conversion response matching current API spec."""
    return {
        "success": True,
        "task_id": "wav-task-123",
        "trace_id": "wav-trace-456",
        "data": [
            {
                "file_url": "https://platform.cdn.acedata.cloud/suno/test-audio.wav",
            }
        ],
    }


@pytest.fixture
def mock_midi_response():
    """Mock MIDI conversion response matching current API spec."""
    return {
        "success": True,
        "task_id": "midi-task-123",
        "trace_id": "midi-trace-456",
        "data": [
            {
                "file_url": "https://cdn1.suno.ai/test-audio.midi",
            }
        ],
    }


@pytest.fixture
def mock_vox_response():
    """Mock vocal extraction response matching current API spec."""
    return {
        "success": True,
        "task_id": "vox-task-123",
        "trace_id": "vox-trace-456",
        "data": {
            "id": "vox-id-789",
            "status": "complete",
            "vocal_audio_url": "https://cdn1.suno.ai/processed_test_vocals.m4a",
        },
    }


@pytest.fixture
def mock_style_response():
    """Mock style optimization response."""
    return {
        "success": True,
        "data": {
            "text": "upbeat pop rock, energetic drums, catchy electric guitar riffs, anthemic chorus",
        },
    }


@pytest.fixture
def mock_upload_response():
    """Mock upload response."""
    return {
        "success": True,
        "data": {
            "id": "upload-id-789",
        },
    }

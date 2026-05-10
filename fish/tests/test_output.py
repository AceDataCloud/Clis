"""Tests for output formatting."""

from fish_cli.core.output import (
    DEFAULT_AUDIO_FORMAT,
    DEFAULT_LATENCY_MODE,
    DEFAULT_TTS_MODEL,
    FISH_AUDIO_FORMATS,
    FISH_LATENCY_MODES,
    FISH_MP3_BITRATES,
    FISH_TTS_MODELS,
)


class TestOutputConstants:
    """Tests for output module constants."""

    def test_tts_models(self):
        assert "s2-pro" in FISH_TTS_MODELS
        assert "s1" in FISH_TTS_MODELS

    def test_default_tts_model(self):
        assert DEFAULT_TTS_MODEL == "s2-pro"

    def test_audio_formats(self):
        assert "mp3" in FISH_AUDIO_FORMATS
        assert "wav" in FISH_AUDIO_FORMATS
        assert "pcm" in FISH_AUDIO_FORMATS
        assert "opus" in FISH_AUDIO_FORMATS

    def test_default_audio_format(self):
        assert DEFAULT_AUDIO_FORMAT == "mp3"

    def test_mp3_bitrates(self):
        assert 64 in FISH_MP3_BITRATES
        assert 128 in FISH_MP3_BITRATES
        assert 192 in FISH_MP3_BITRATES

    def test_latency_modes(self):
        assert "normal" in FISH_LATENCY_MODES
        assert "balanced" in FISH_LATENCY_MODES

    def test_default_latency_mode(self):
        assert DEFAULT_LATENCY_MODE == "normal"

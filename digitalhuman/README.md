# Digital Human CLI

A command-line tool for the [AceDataCloud](https://platform.acedata.cloud) Digital Human API.

## Installation

```bash
pip install digitalhuman-cli
```

## Quick Start

```bash
export ACEDATACLOUD_API_TOKEN=your_token

# Generate a digital human video
digitalhuman generate --video-url https://example.com/face.mp4 \
                      --audio-url https://example.com/speech.mp3

# You can also use a still image as the face source
digitalhuman generate --image-url https://example.com/portrait.jpg \
                      --audio-url https://example.com/speech.mp3

# Clone a voice first, then use it for TTS
digitalhuman clone-voice --audio-url https://example.com/voice.wav
digitalhuman generate --video-url https://example.com/face.mp4 \
                      --text "Hello world" --voice-id f754a190e26c

# Check task status
digitalhuman task task_49af42c410c24f04ad416b28af55d237

# Wait for completion
digitalhuman wait task_abc123
```

## Commands

- `generate` – Generate a digital human video from a face source and audio/text
- `clone-voice` – Clone a voice from an audio sample
- `task` – Query a single task status
- `tasks` – Query multiple tasks
- `wait` – Poll until a task completes
- `engines` – List available engines
- `config` – Show current configuration

## Notes

- `--engine` is still accepted for backward compatibility, but no longer changes the output or pricing.
- `--resolution` is still accepted for backward compatibility, but output is always rendered at 720p.

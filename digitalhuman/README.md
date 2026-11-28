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
- `tasks` – List recent history, or retrieve each supplied task ID individually
- `wait` – Poll until a task completes
- `engines` – List available engines
- `config` – Show current configuration

## Task history and selected IDs

```bash
digitalhuman tasks --limit 20 --type videos --json
digitalhuman tasks --created-at-min 1793404800 --created-at-max 1793491200 --json
digitalhuman tasks task_abc123 task_def456 --json
```

With no IDs, `tasks` lists the authenticated caller's recent history, newest first.
`--limit` is 1–100 (server default: 20), `--type` is `videos` or `voices`, and
creation filters are strict Unix-second boundaries. The API's `retrieve_batch`
action lists history; it does not look up an array of IDs.

With IDs, the CLI sends one `retrieve` request per ID and collects them into
`items` and `count`. History filters cannot be combined with selected IDs.
Detailed task records carry timing/status fields and nest video or voice output
inside `response`; `--json` preserves the full records, including null timing fields.

## Notes

- `--engine` is still accepted for backward compatibility, but no longer changes the output or pricing.
- `--resolution` is still accepted for backward compatibility, but output is always rendered at 720p.

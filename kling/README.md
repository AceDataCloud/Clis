# Kling CLI

A command-line tool for Kling AI Video Generation via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install kling-pro-cli
```

## Usage

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Generate a video from a text prompt
kling generate "A cinematic scene of a sunset over the ocean"

# Generate a video from a reference image
kling image-to-video "Animate this scene" --start-image-url https://example.com/photo.jpg

# Extend an existing video
kling extend --video-id abc123

# Generate a motion video from image + reference video
kling motion --image-url https://example.com/img.jpg --video-url https://example.com/ref.mp4

# Apply lip sync to a video with audio
kling lip-sync --mode audio2video --video-url https://example.com/video.mp4 --audio-url https://example.com/audio.mp3

# Apply lip sync to a video using text-to-speech
kling lip-sync --mode text2video --video-id abc123 --text "Hello world" --voice-language en

# Animate a photo with synchronized audio
kling talking-photo --image-url https://example.com/photo.jpg --audio-url https://example.com/speech.mp3

# Check task status
kling task abc123-def456

# Wait for a task to complete
kling wait abc123 --interval 5

# List available models
kling models

# Show configuration
kling config
```

## Options

- `--token` / `ACEDATACLOUD_API_TOKEN` — API token
- `--json` — Output raw JSON

## Models

| Model | Notes |
|-------|-------|
| kling-v1 | Default model |
| kling-v1-6 | Version 1.6 |
| kling-v2-5-turbo | Version 2.5 Turbo |
| kling-v2-6 | Version 2.6 |
| kling-v3 | Version 3 (supports 4K mode) |
| kling-v3-omni | Version 3 Omni (supports 4K mode) |
| kling-video-o1 | Video O1 |
| kling-v2-master | Version 2 Master |
| kling-v2-1-master | Version 2.1 Master |

## License

MIT

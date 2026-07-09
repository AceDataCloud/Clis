# HappyHorse CLI

A command-line tool for AI video generation using HappyHorse through the AceDataCloud platform.

## Installation

```bash
pip install happyhorse-cli
```

## Usage

```bash
# Set API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Generate video from text
happyhorse generate "A horse galloping through a field"

# Generate video from image
happyhorse image-to-video "Animate this scene" --image-url https://example.com/photo.jpg

# Generate video from reference images
happyhorse reference-to-video "Create scene" --image-urls https://example.com/ref.jpg

# Edit a video
happyhorse video-edit "Add dramatic music" --video-url https://example.com/video.mp4

# Check task status
happyhorse task abc123-def456

# Wait for task completion
happyhorse wait abc123 --interval 5

# List available models
happyhorse models

# Show configuration
happyhorse config
```

## Options

### generate

| Option | Default | Description |
|--------|---------|-------------|
| `--model` | `happyhorse-1.1-t2v` | Model to use |
| `--resolution` | `1080P` | Video resolution (720P, 1080P) |
| `--ratio` | `16:9` | Aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4) |
| `--duration` | `5` | Duration in seconds |
| `--watermark` | `False` | Add watermark |
| `--audio-setting` | `auto` | Audio setting (auto, origin) |
| `--seed` | None | Random seed |
| `--callback-url` | None | Webhook callback URL |
| `--async` | `False` | Submit asynchronously |
| `--json` | `False` | Output raw JSON |

## Models

| Model | Type |
|-------|------|
| `happyhorse-1.0-t2v` | Text-to-Video |
| `happyhorse-1.1-t2v` | Text-to-Video (default) |
| `happyhorse-1.0-i2v` | Image-to-Video |
| `happyhorse-1.1-i2v` | Image-to-Video |
| `happyhorse-1.0-r2v` | Reference-to-Video |
| `happyhorse-1.1-r2v` | Reference-to-Video |
| `happyhorse-1.0-video-edit` | Video Edit |

## License

MIT

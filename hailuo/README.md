# Hailuo CLI

A command-line tool for generating AI videos using [Hailuo (MiniMax)](https://platform.acedata.cloud) through the AceDataCloud platform.

## Installation

```bash
pip install hailuo-cli
```

## Configuration

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or copy `.env.example` to `.env` and fill in your token.

## Commands

### Video Generation

| Command | Description |
|---------|-------------|
| `hailuo generate <prompt>` | Generate a video from text (minimax-t2v) |
| `hailuo image-to-video <prompt> --image-url <url>` | Generate video from image + text |

### Task Management

| Command | Description |
|---------|-------------|
| `hailuo task <task_id>` | Query a single task status |
| `hailuo tasks <id1> <id2> [...]` | Query multiple tasks at once |
| `hailuo wait <task_id>` | Wait for task completion with polling |

### Utilities

| Command | Description |
|---------|-------------|
| `hailuo models` | List available Hailuo models |
| `hailuo config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--callback-url  Webhook URL for async notifications
```

## Examples

```bash
# Generate a video from a text prompt
hailuo generate "A cat playing in the snow"

# Generate from image reference
hailuo image-to-video "Animate the scene" --image-url https://example.com/photo.jpg

# Use a specific model
hailuo generate "Ocean waves" --model minimax-t2v

# Director model with image reference
hailuo image-to-video "Cinematic pan" --image-url img.jpg --model minimax-i2v-director

# Check task status
hailuo task abc123-def456

# Wait for completion
hailuo wait abc123 --timeout 300
```

## Docker

```bash
# Pull the image
docker pull ghcr.io/acedatacloud/hailuo-cli:latest

# Run a command
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/hailuo-cli generate "A happy scene"

# Or use docker-compose
docker compose run --rm hailuo-cli generate "A happy scene"
```

## Project Structure

```
HailuoCli/
├── hailuo_cli/             # Main package
│   ├── __init__.py
│   ├── __main__.py         # python -m hailuo_cli entry point
│   ├── main.py             # CLI entry point
│   ├── core/               # Core modules
│   │   ├── client.py       # HTTP client for Hailuo API
│   │   ├── config.py       # Configuration management
│   │   ├── exceptions.py   # Custom exceptions
│   │   └── output.py       # Rich terminal formatting
│   └── commands/           # CLI command groups
│       ├── video.py        # Video generation commands
│       ├── task.py         # Task management commands
│       └── info.py         # Info and utility commands
└── tests/                  # Test suite
```

## License

MIT License — see [LICENSE](LICENSE) for details.

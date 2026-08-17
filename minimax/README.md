# MiniMax CLI

A command-line tool for generating AI videos using [MiniMax](https://platform.acedata.cloud) through the AceDataCloud platform.

## Installation

```bash
pip install minimax-cli
```

## Configuration

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or copy `.env.example` to `.env` and fill in your token.

Generation waits for the completed video by default. Pass `--async` to return a task ID immediately, then use `minimax task` / `minimax wait` to retrieve the result. Providing `--callback-url` also enables asynchronous generation.

## Commands

### Video Generation

| Command | Description |
|---------|-------------|
| `minimax generate <prompt>` | Generate a video from text (MiniMax-H3) |
| `minimax image-to-video <prompt> --image-url <url>` | Generate video from image + text |

### Task Management

| Command | Description |
|---------|-------------|
| `minimax task <task_id>` | Query a single task status |
| `minimax tasks <id1> <id2> [...]` | Query multiple tasks at once |
| `minimax delete <task_id>` | Delete a task |
| `minimax wait <task_id>` | Wait for task completion with polling |

### Utilities

| Command | Description |
|---------|-------------|
| `minimax models` | List available MiniMax models |
| `minimax config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--async         Return immediately with a task ID
--callback-url  Webhook URL for async notifications
```

## Examples

```bash
# Generate a video from a text prompt
minimax generate "A cat playing in the snow"

# Generate from image reference
minimax image-to-video "Animate the scene" --image-url https://example.com/photo.jpg

# Use a specific model
minimax generate "Ocean waves" --model MiniMax-H3

# Check task status
minimax task abc123-def456

# Wait for completion
minimax wait abc123 --timeout 300
```

## Docker

```bash
# Pull the image
docker pull ghcr.io/acedatacloud/minimax-cli:latest

# Run a command
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/minimax-cli generate "A happy scene"

# Or use docker-compose
docker compose run --rm minimax-cli generate "A happy scene"
```

## Project Structure

```
MiniMaxCli/
├── minimax_cli/             # Main package
│   ├── __init__.py
│   ├── __main__.py         # python -m minimax_cli entry point
│   ├── main.py             # CLI entry point
│   ├── core/               # Core modules
│   │   ├── client.py       # HTTP client for MiniMax API
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

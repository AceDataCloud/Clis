# Midjourney CLI

[![PyPI version](https://img.shields.io/pypi/v/midjourney-pro-cli.svg)](https://pypi.org/project/midjourney-pro-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/midjourney-pro-cli.svg)](https://pypi.org/project/midjourney-pro-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/MidjourneyCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/MidjourneyCli/actions/workflows/ci.yaml)

A command-line tool for AI image and video generation using [Midjourney](https://www.midjourney.com/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI images, edit photos, create videos, and manage tasks directly from your terminal — no MCP client required.

## Features

- **Image Generation** — Generate from prompts, transform (upscale/variation/zoom/pan), blend images
- **Image Editing** — Edit with prompts and masks, describe images (reverse prompt), translate prompts
- **Video Generation** — Generate video from text + reference image, extend existing videos
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping
- **Multiple Modes** — fast, turbo, relax generation modes
- **V8 Support** — HD mode, ultra quality, style references

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to [Midjourney API](https://platform.acedata.cloud/documents/c0dbabae-3f91-470f-abb1-22e9ed2753e8)
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install midjourney-pro-cli

# Or with uv (recommended)
uv pip install midjourney-pro-cli

# Or from source
git clone https://github.com/AceDataCloud/MidjourneyCli.git
cd MidjourneyCli
pip install -e .
```

### 3. Configure

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Or use .env file
cp .env.example .env
# Edit .env with your token
```

### 4. Use

```bash
# Generate an image
midjourney imagine "A majestic lion at sunset, cinematic lighting"

# Generate with V8 HD mode
midjourney imagine "Cyberpunk city" --version 8 --hd --mode turbo

# Upscale a specific image from the grid
midjourney transform <image_id> upscale1

# Edit an existing image
midjourney edit https://example.com/photo.jpg "Add a sunset background"

# Describe an image (reverse prompt)
midjourney describe https://example.com/photo.jpg

# Generate video
midjourney video "A cat walking" --image-url https://example.com/cat.jpg

# Check task status
midjourney task <task_id>

# Wait for completion
midjourney wait <task_id> --interval 5
```

## Commands

### Image Generation

| Command | Description |
|---------|-------------|
| `midjourney imagine <prompt>` | Generate a 2x2 grid of images from text |
| `midjourney transform <image_id> <action>` | Upscale, vary, zoom, or pan an image |
| `midjourney blend <url1> <url2> [...]` | Blend 2-5 images together |

### Image Editing

| Command | Description |
|---------|-------------|
| `midjourney edit <image_url> <prompt>` | Edit an image with a text prompt |
| `midjourney describe <image_url>` | Get 4 AI descriptions of an image |
| `midjourney translate <content>` | Translate Chinese text to English prompts |

### Video Generation

| Command | Description |
|---------|-------------|
| `midjourney video <prompt> --image-url <url>` | Generate video from text + image |
| `midjourney extend-video <video_id> <prompt>` | Extend an existing video |

### Task Management

| Command | Description |
|---------|-------------|
| `midjourney task <task_id>` | Query a single task status |
| `midjourney tasks <id1> <id2> [...]` | Query multiple tasks at once |
| `midjourney wait <task_id>` | Wait for task completion with polling |
| `midjourney seed <image_id>` | Get the seed value of a generated image |

### Utilities

| Command | Description |
|---------|-------------|
| `midjourney modes` | List available generation modes |
| `midjourney versions` | List available Midjourney versions |
| `midjourney actions` | List available transform actions |
| `midjourney config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--mode TEXT     Generation mode: fast (default), turbo, relax
```

## Transform Actions

After generating a 2x2 grid with `imagine`:

| Action | Description |
|--------|-------------|
| `upscale1-4` | Upscale one of the 4 grid images |
| `upscale_2x` / `upscale_4x` | Further upscale an upscaled image |
| `variation1-4` | Create variations of one grid image |
| `variation_subtle` / `variation_strong` | Create subtle/strong variations |
| `variation_region` | Edit specific region with mask |
| `reroll` | Regenerate all 4 images |
| `zoom_out_2x` / `zoom_out_1_5x` | Zoom out |
| `pan_left/right/up/down` | Expand image in a direction |

## Scripting & Piping

The `--json` flag outputs machine-readable JSON suitable for piping:

```bash
# Generate and extract task ID
TASK_ID=$(midjourney imagine "sunset" --json | jq -r '.task_id')

# Wait for completion and get image URL
midjourney wait $TASK_ID --json | jq -r '.image_url'

# Batch generate from a file of prompts
while IFS= read -r prompt; do
  midjourney imagine "$prompt" --json >> results.jsonl
done < prompts.txt
```

## Available Versions

| Version | Notes |
|---------|-------|
| `5.2` | Stable, well-tested |
| `6` | Improved prompt understanding |
| `6.1` | Enhanced detail and coherence |
| `7` | Better composition and realism |
| `8` | Latest V8 Alpha — HD and ultra quality support |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `MIDJOURNEY_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/MidjourneyCli.git
cd MidjourneyCli

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=midjourney_cli

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy midjourney_cli
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Docker

```bash
# Pull the image
docker pull ghcr.io/acedatacloud/midjourney-cli:latest

# Run a command
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/midjourney-cli imagine "A happy scene"

# Or use docker-compose
docker compose run --rm midjourney-cli imagine "A happy scene"
```

## Project Structure

```
MidjourneyCli/
├── midjourney_cli/         # Main package
│   ├── __init__.py
│   ├── __main__.py        # python -m midjourney_cli entry point
│   ├── main.py            # CLI entry point
│   ├── core/              # Core modules
│   │   ├── client.py      # HTTP client for Midjourney API
│   │   ├── config.py      # Configuration management
│   │   ├── exceptions.py  # Custom exceptions
│   │   └── output.py      # Rich terminal formatting
│   └── commands/          # CLI command groups
│       ├── imagine.py     # Image generation (imagine, transform, blend)
│       ├── edit.py        # Edit, describe, translate commands
│       ├── video.py       # Video generation commands
│       ├── task.py        # Task management commands
│       └── info.py        # Info & utility commands
├── tests/                  # Test suite
├── Dockerfile             # Container image
├── .env.example           # Environment template
├── pyproject.toml         # Project configuration
└── README.md
```

## Midjourney CLI vs MCP Midjourney

| Feature | Midjourney CLI | MCP Midjourney |
|---------|---------------|----------------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install midjourney-pro-cli` | `pip install mcp-midjourney` |

Both tools use the same AceDataCloud API and share the same API token.

## API Reference

This tool wraps the [AceDataCloud Midjourney API](https://platform.acedata.cloud/documents/c0dbabae-3f91-470f-abb1-22e9ed2753e8):

- [Midjourney Imagine API](https://platform.acedata.cloud/documents/c0dbabae-3f91-470f-abb1-22e9ed2753e8) — Image generation
- [Midjourney Edits API](https://platform.acedata.cloud/documents/0c9f39ff-08a5-4a69-8772-80e48b0db9f0) — Image editing
- [Midjourney Videos API](https://platform.acedata.cloud/documents/60f6e9cd-09d1-4dab-abe0-4fb95e65e687) — Video generation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud/)
- [MCP Midjourney](https://github.com/AceDataCloud/MidjourneyMCP) — MCP server version
- [Midjourney Official](https://www.midjourney.com/)

---

Made with ❤️ by [AceDataCloud](https://platform.acedata.cloud/)
